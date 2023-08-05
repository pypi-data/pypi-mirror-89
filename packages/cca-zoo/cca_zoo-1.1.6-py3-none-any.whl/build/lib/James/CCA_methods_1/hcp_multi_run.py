import os
import json
from CCA_methods.generate_data import *
from CCA_methods.hcp_utils import load_hcp_data, score_feat_corr, reduce_dimensions
from CCA_methods.plot_utils import plot_connectome_correlations, plot_weights, plot_results
import CCA_methods

def main():
    # This runs
    home_dir = os.getcwd()
    debug = False
    subjects = '1000'
    runs = 10
    max_als_iter = 100
    outdim_size = 2
    cv_folds = 5
    epoch_num = 100

    if debug:
        #view_1, view_2, _,_ = generate_mai(1000, outdim_size, 100, 100, 1, 1)
        view_1, view_2, _, _ = generate_candola(1000, outdim_size, 100, 100, 1, 1)
        # view_1 = np.random.rand(1000, 100)
        # view_2 = np.random.rand(1000, 100)
        view_1 -= view_1.mean(axis=0)
        view_2 -= view_2.mean(axis=0)
        np.save('view_1', view_1)
        np.save('view_2', view_2)
        original_brain = view_1
        num_subjects = original_brain.shape[0]
    else:
        brain, behaviour, original_brain, original_behaviour, original_brain_triu, data_dict, smith_cats = load_hcp_data(
            subjects=subjects)
        # Unpacking the data
        view_1 = brain.astype(np.float32)
        view_2 = behaviour.astype(np.float32)
        num_subjects = view_1.shape[0]

    for run in range(runs):
        # Simple
        if not os.path.exists(home_dir + '/run_' + str(run)):
            os.makedirs(home_dir + '/run_' + str(run))
        os.chdir(home_dir + '/run_' + str(run))
        all_inds = np.arange(num_subjects)
        np.random.shuffle(all_inds)
        train_inds, test_inds = np.split(all_inds, [int(round(0.8 * num_subjects, 0))])

        train_set_1 = view_1[train_inds]
        train_set_2 = view_2[train_inds]
        test_set_1 = view_1[test_inds]
        test_set_2 = view_2[test_inds]
        train_set_1_conv = np.reshape(original_brain[train_inds], (
            -1, int(np.sqrt(original_brain.shape[1])), int(np.sqrt(original_brain.shape[1])), 1))
        test_set_1_conv = np.reshape(original_brain[test_inds], (
            -1, int(np.sqrt(original_brain.shape[1])), int(np.sqrt(original_brain.shape[1])), 1))
        if not debug:
            train_set_1, train_set_2, test_set_1, test_set_2 = reduce_dimensions(train_set_1, train_set_2,
                                                                                 test_x=test_set_1,
                                                                                 test_y=test_set_2)

        # GPCCA
        #gp = CCA_methods.gaussian_process_cca.Wrapper(outdim_size=2, sparse_x=False, sparse_y=False, steps_gpcca=2000,
        #                                              steps_gp_y=2000,
        #                                              steps_gp_z=2000,noise=1)

        #gp.fit(train_set_1, train_set_2)

        #gp_results = np.stack((gp.train_correlations, gp.predict_corr(test_set_1, test_set_2)))

        """
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(gp.gp_y_losses)
        plt.figure()
        plt.plot(gp.gp_z_losses)
        plt.figure()
        plt.plot(gp.gpcca_losses)
        plt.figure()
        plt.scatter(gp.U[0], gp.V[0])
        plt.figure()
        plt.scatter(gp.U[1], gp.V[1])
        plt.show()
"""

        ## Scikit-learn
        scikit = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='scikit', max_iter=max_als_iter).fit(
            train_set_1,
            train_set_2)

        scikit_results = np.stack(
            (scikit.train_correlations, scikit.predict_corr(test_set_1, test_set_2)))

        # CCA_archive with ALS:
        params = {'c_1': 0, 'c_2': 0}
        als = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='l2', params=params,
                                             max_iter=max_als_iter).fit(
            train_set_1,
            train_set_2)
        als_results = np.stack((als.train_correlations, als.predict_corr(test_set_1, test_set_2)))

        # kernel cca
        params = {'reg': 1e+4}
        kernel_linear = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='kernel',
                                                       max_iter=max_als_iter, params=params).fit(train_set_1,
                                                                                                       train_set_2)
        kernel_linear_results = np.stack(
            (kernel_linear.train_correlations, kernel_linear.predict_corr(test_set_1, test_set_2)))

        # r-kernel cca
        param_candidates = {'reg': [1e+4, 1e+5, 1e+6]}
        kernel_reg = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='kernel',
                                                    max_iter=max_als_iter, params=params).cv_fit(train_set_1,
                                                                                                       train_set_2,
                                                                                                       folds=cv_folds,
                                                                                                       param_candidates=param_candidates)
        kernel_reg_results = np.stack(
            (kernel_reg.train_correlations, kernel_reg.predict_corr(test_set_1, test_set_2)))

        with open("kernel_reg.json", "a") as f:
            json.dump(kernel_reg.params, f)

        # kernel cca (gaussian)
        param_candidates = {'kernel': ['gaussian'], 'sigma': [100, 200, 300], 'reg': [1e+3, 1e+4, 1e+5]}

        kernel_gaussian = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='kernel', max_iter=max_als_iter).cv_fit(train_set_1, train_set_2, folds=cv_folds,
                                                                                                                                 param_candidates=param_candidates)

        kernel_gaussian_results = np.stack(
            (kernel_gaussian.train_correlations, kernel_gaussian.predict_corr(test_set_1, test_set_2)))

        with open("kernel_gaussian.json", "a") as f:
            json.dump(kernel_gaussian.params, f)

        # kernel cca (poly)
        param_candidates = {'kernel': ['poly'], 'degree': [2, 3, 4], 'reg': [1e+3, 1e+4, 1e+5]}

        kernel_poly = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='kernel', max_iter=max_als_iter).cv_fit(train_set_1, train_set_2, folds=cv_folds,
                                                                                                                             param_candidates=param_candidates)

        kernel_poly_results = np.stack(
            (kernel_poly.train_correlations, kernel_poly.predict_corr(test_set_1, test_set_2)))

        with open("kernel_poly.json", "a") as f:
            json.dump(kernel_poly.params, f)

        # Regularized ALS
        param_candidates = {'c_1': [0.1, 1, 10, 100], 'c_2': [0.1, 1, 10, 100]}

        ridge_als = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='l2', max_iter=max_als_iter).cv_fit(train_set_1, train_set_2,
                                                                                                                       param_candidates=param_candidates,
                                                                                                                       folds=cv_folds)

        ridge_als_results = np.stack(
            (ridge_als.train_correlations, ridge_als.predict_corr(test_set_1, test_set_2)))

        with open("reg_als.json", "a") as f:
            json.dump(ridge_als.params, f)

        # Sparse ALS
        param_candidates = {'c_1': [0.00001,0.0001, 0.001], 'c_2': [0.00001,0.0001, 0.001]}

        sparse_als = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='scca',
                                                    max_iter=max_als_iter).cv_fit(train_set_1,
                                                                                        train_set_2,
                                                                                        param_candidates=param_candidates,
                                                                                        folds=cv_folds, verbose=True)

        sparse_als_results = np.stack(
            (sparse_als.train_correlations,
             sparse_als.predict_corr(test_set_1, test_set_2)))

        with open("sparse_als.json", "a") as f:
            json.dump(sparse_als.params, f)

        # Sparse Generalized ALS
        param_candidates = {'c_1': [0.00001, 0.0001, 0.001], 'c_2': [0.00001, 0.0001, 0.001]}

        sparse_generalized_als = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='sgcca',
                                                                max_iter=max_als_iter).cv_fit(train_set_1,
                                                                              train_set_2,
                                                                              param_candidates=param_candidates,
                                                                              folds=cv_folds, verbose=True)

        sparse_generalized_als_results = np.stack(
            (sparse_generalized_als.train_correlations,
             sparse_generalized_als.predict_corr(test_set_1, test_set_2)))

        with open("sparse_generalized_als.json", "a") as f:
            json.dump(sparse_generalized_als.params, f)

        # PMD
        param_candidates = {'c_1': [1, 3, 7, 9], 'c_2': [1, 3, 7, 9]}

        pmd = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='pmd',
                                             max_iter=max_als_iter).cv_fit(train_set_1, train_set_2,
                                                                                 param_candidates=param_candidates,
                                                                                 folds=cv_folds)

        pmd_results = np.stack(
            (pmd.train_correlations, pmd.predict_corr(test_set_1, test_set_2)))

        with open("pmd.json", "a") as f:
            json.dump(pmd.params, f)

        # Parkhomenko
        param_candidates = {'c_1': [0.01, 0.02, 0.03, 0.04], 'c_2': [0.01, 0.02, 0.03, 0.04]}

        parkohomenko = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='parkhomenko',
                                                      max_iter=max_als_iter).cv_fit(train_set_1,
                                                                                          train_set_2,
                                                                                          param_candidates=param_candidates,
                                                                                          folds=cv_folds)

        parkohomenko_results = np.stack(
            (parkohomenko.train_correlations, parkohomenko.predict_corr(test_set_1, test_set_2)))

        with open("sparse_parkohomenko.json", "a") as f:
            json.dump(parkohomenko.params, f)

        # Sparse ALS (elastic)
        param_candidates = {'c_1': [0.01, 0.1, 1], 'c_2': [0.01, 0.1, 1], 'l1_ratio_1': [0.001, 0.01, 0.1],
                            'l1_ratio_2': [0.01, 0.01, 0.1]}

        elastic_als = CCA_methods.linear.DeepWrapper(outdim_size=outdim_size, method='elastic',
                                                     max_iter=max_als_iter).cv_fit(train_set_1, train_set_2,
                                                                  param_candidates=param_candidates,
                                                                  folds=cv_folds)

        elastic_als_results = np.stack(
            (elastic_als.train_correlations, elastic_als.predict_corr(test_set_1, test_set_2)))

        with open("sparse_waaijenborg.json", "a") as f:
            json.dump(elastic_als.params, f)

        # Deep FCN Torch
        deep = CCA_methods.deep.DeepWrapper(outdim_size=outdim_size, epoch_num=epoch_num)

        deep.fit(train_set_1, train_set_2)

        deep_results = np.stack((deep.train_correlations, deep.predict_corr(test_set_1, test_set_2)))

        all_results = np.stack(
            [scikit_results, als_results, ridge_als_results, pmd_results, parkohomenko_results, sparse_als_results, sparse_generalized_als_results,
             elastic_als_results, kernel_linear_results, kernel_reg_results, kernel_gaussian_results,
             kernel_poly_results,
             deep_results],
            axis=0)
        all_labels = ['NIPALS', 'ALS', 'Ridge - ALS', 'PMD', 'Parkhomenko', 'Sparse - ALS','Sparse - Generalized ALS',
                      'Elastic - ALS', 'KCCA', 'KCCA-reg', 'KCCA-gaussian', 'KCCA-polynomial', 'DCCA']

        plot_results(all_results, all_labels)

        all_w_weights = np.stack(
            [scikit.W, als.W, ridge_als.W, pmd.W, parkohomenko.W, sparse_als.W,sparse_generalized_als.W,
             elastic_als.W],
            axis=0)

        all_c_weights = np.stack(
            [scikit.C, als.C, ridge_als.C, pmd.C, parkohomenko.C, sparse_als.C,sparse_generalized_als.C,
             elastic_als.C],
            axis=0)

        all_u = np.stack(
            [scikit.U, als.U, ridge_als.U, pmd.U, parkohomenko.U, sparse_als.U,sparse_generalized_als.U,
             elastic_als.U],
            axis=0)

        all_v = np.stack(
            [scikit.V, als.V, ridge_als.V, pmd.V, parkohomenko.V, sparse_als.V,sparse_generalized_als.V,
             elastic_als.V],
            axis=0)

        np.save('w_weights', all_w_weights)
        np.save('c_weights', all_c_weights)
        np.save('u', all_u)
        np.save('v', all_v)
        np.save('results', all_results)
        np.save('train_ids', train_inds)
        np.save('test_ids', test_inds)

    if not debug:
        ordered_connectivity, cca_connectivity, linkage, behaviour_output = score_feat_corr(als.U,
                                                                                            als.V,
                                                                                            original_brain_triu[
                                                                                                train_inds],
                                                                                            original_behaviour.iloc[
                                                                                                train_inds],
                                                                                            data_dict,
                                                                                            smith_cats)
        print(behaviour_output.head(20), flush=True)

        print(behaviour_output.tail(20), flush=True)

        behaviour_output.to_csv('corrs_out.csv')

        plot_connectome_correlations(ordered_connectivity, cca_connectivity, linkage)

        plot_weights(als.W, als.C)


if __name__ == "__main__":
    main()
