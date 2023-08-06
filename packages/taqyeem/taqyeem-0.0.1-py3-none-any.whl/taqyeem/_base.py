from collections import Iterable
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from tabulate import tabulate


class TaqExperiment:
    def __init__(self, name: str = "default_experiment", log_filepath: str = None, verbose: int = 10):
        """ Initialize a new Experiment instance

        Parameters
        ----------
        name: str
            Experiment name
        log_filepath: str
            Log file path
        verbose: int
            logging verbose level
        """
        self.name = name
        self._models = set()
        self._results = pd.DataFrame(columns=['model'])
        self._configs = set()
        self._metrics = set()
        self._hparams = set()
        self._report = None
        self.__cv_summary = pd.DataFrame(columns=['model'])

        self._verbose = verbose
        self.__events = dict()

        self._logger = self._logger = logging.getLogger("taqyeem")
        self._init_logger(log_filepath)

    def _init_logger(self, log_filepath: str = None):
        self._logger.setLevel(self._verbose)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(f"[%(asctime)s - %(name)s - {self.name} - %(levelname)s => %(message)s")
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._log_filepath = log_filepath
        if self._log_filepath is not None:
            fh = logging.FileHandler(self._log_filepath)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

    def add_configs(self, configs: Iterable):
        """ Add a configuration to the experiment

        Parameters
        ----------
        configs: Iterable
            Configuration names to be added to the experiments.
        """
        for c_name in configs:
            self._configs.add(c_name)
        self._rebuild_result_data()

    @property
    def configs(self) -> list:
        """ Experiment configurations

        Returns
        -------
        dict
            Experiment configs and their values
        """
        return list(self._configs)

    @property
    def metrics(self) -> list:
        """ Experiment metrics

        Returns
        -------
        dict
            Experiment metrics
        """
        return list(self._metrics)

    @property
    def hparams(self) -> list:
        """ Experiment hparams

        Returns
        -------
        dict
            Experiment hparams
        """
        return list(self._hparams)

    @property
    def models(self) -> list:
        """ Experiment models

        Returns
        -------
        dict
            Experiment models
        """
        return list(self._models)

    def start_experiment(self):
        now_time = datetime.now()
        self.__events['exp_start'] = now_time
        self._logger.debug(f"experiment started")

    def end_experiment(self):
        now_time = datetime.now()
        self.__events['exp_end'] = now_time
        duration = self.__events['exp_end'] - self.__events['exp_start']
        self._logger.debug(f"experiment ended - duration: {duration}")

    def _rebuild_result_data(self):
        all_cols = set.union(self._configs, self._metrics, self._hparams)
        current_cols = set(self._results.columns)
        new_cols = all_cols.difference(current_cols)
        for col in new_cols:
            self._results[col] = np.nan

    def submit_results(self, model_name: str, metrics: dict, configs: dict = None, hparam: dict = None):
        """

        Parameters
        ----------
        model_name: str
            Model name
        metrics: dict
            Dictionary of results where metric names are keys and their scores are values
        configs: dict
            Configurations associated to this result
        hparam: dict
            Model hyper-parameters related to the submitted results
        """
        if model_name not in self._models:
            self._models.add(model_name)

        results_record = {"model": model_name}
        results_record.update(metrics)
        results_record.update(configs) if configs is not None else None
        results_record.update(hparam) if hparam is not None else None

        config_names = list(configs.keys())
        metric_names = list(metrics.keys())
        for c_name in config_names:
            if c_name not in self._configs:
                self._configs.add(c_name)
        for m_name in metric_names:
            if m_name not in self._metrics:
                self._metrics.add(m_name)
        self._rebuild_result_data()
        self._results = self._results.append(results_record, ignore_index=True)
        self._logger.debug(f" = RESULTS = model: {model_name} - config: {configs} - metrics: {metrics} - hparams: {hparam}")

    def generate_summary_report(self, selected_configs: Iterable = None, selected_metrics: Iterable = None, selected_hparams: Iterable = None):
        selected_configs = self.configs if selected_configs is None else selected_configs
        selected_metrics = self.metrics if selected_metrics is None else selected_metrics
        selected_hparams = self.hparams if selected_hparams is None else selected_hparams

        headers = ["model"] + selected_configs + selected_metrics + selected_hparams
        results_df = self._results[headers]
        return tabulate(results_df, headers='keys', tablefmt='psql', numalign="center", floatfmt="1.3f", showindex=False)

    @property
    def report(self):
        return self.generate_summary_report()

    def __repr__(self):
        return self.generate_summary_report(self.configs, self.metrics, self.hparams)


class TaqKfoldCVExperiment(TaqExperiment):

    def __init__(self, name: str = "default_experiment", log_filepath: str = None, verbose: int = 10):
        super(TaqKfoldCVExperiment, self).__init__(name=name, log_filepath=log_filepath, verbose=verbose)
        self._configs.update({"run", "fold"})
        self._rebuild_result_data()

        self._results['run'] = self._results['run'].astype(int)
        self._results['fold'] = self._results['fold'].astype(int)

        self.__cv_report = pd.DataFrame(columns=["run", "model"])

    @property
    def runs(self):
        return np.array([v for v in self._results['run'].unique() if v is not np.nan])

    def submit_cv_results(self, model_name: str, run_index: int, fold_index: int, metrics: dict, configs: dict = None, hparam: dict = None):
        """ Submit cross validation results

        Parameters
        ----------
        model_name: str
            Model
        run_index: int
            K-fold cross validation run index
        fold_index: int
            K-fold cross validation fold index
        metrics: dict
            Dictionary of results where metric names are keys and their scores are values
        configs: dict
            Configurations associated to this result
        hparam: dict
            Model hyper-parameters related to the submitted results
        """
        configs['run'] = run_index
        configs['fold'] = fold_index
        self.submit_results(model_name, metrics, configs, hparam)

    def __build_cv_report(self):
        headers = ["run", "model"] + self.metrics
        cv_result_summary = pd.DataFrame(columns=headers)
        cv_fold_means = self._results[headers].groupby(['run', 'model']).mean().reset_index()
        cv_fold_stds = self._results[headers].groupby(['run', 'model']).std().reset_index()
        model_runs_means = cv_fold_means[["model"] + self.metrics].groupby("model").mean().reset_index()
        model_runs_stds = cv_fold_means[["model"] + self.metrics].groupby("model").std().reset_index()

        cv_exp_means = cv_fold_means.append(model_runs_means)
        cv_exp_stds = cv_fold_stds.append(model_runs_stds)

        for run_idx in set(cv_fold_means["run"].to_list()):
            for model_name in self.models:
                model_results = {"run": str(run_idx), "model": model_name}
                for mt in self.metrics:
                    mt_mean = cv_exp_means[(cv_exp_means["run"] == run_idx) & (cv_exp_means["model"] == model_name)][mt].to_list()[0]
                    mt_std = cv_exp_stds[(cv_exp_means["run"] == run_idx) & (cv_exp_means["model"] == model_name)][mt].to_list()[0]
                    model_results[mt] = f"{mt_mean:0.3f} (±{mt_std:0.3f})"
                cv_result_summary = cv_result_summary.append(model_results, ignore_index=True)

        for model_name in self.models:
            model_avg_results = {"run": "avg", "model": model_name}
            for mt in self.metrics:
                mt_avg = model_runs_means[model_runs_means['model'] == model_name][mt].to_list()[0]
                mt_std = model_runs_stds[model_runs_means['model'] == model_name][mt].to_list()[0]
                model_avg_results[mt] = f"{mt_avg:0.3f} (±{mt_std:0.3f})"
            cv_result_summary = cv_result_summary.append(model_avg_results, ignore_index=True)
        self.__cv_report = cv_result_summary

    def end_experiment(self):
        self.__build_cv_report()
        super().end_experiment()
        self._logger.debug(f"Cross Validation Report:\n{self.cv_report}")

    @property
    def cv_report(self):
        report_table = tabulate(self.__cv_report, headers='keys', tablefmt='psql', numalign="center", stralign="center", floatfmt="1.3f", showindex=False)
        report_lines = report_table.split("\n")
        hline = report_lines[0]
        headers = report_lines[:2]

        nb_runs = len(self.runs)
        nb_models = len(self.models)

        new_table_lines = headers
        for idx, line in enumerate(report_lines[3:-1]):
            if idx % nb_models == 0:
                new_table_lines.append(hline)
            new_table_lines.append(line)
        new_table_lines.append(hline)
        new_table_txt = "\n".join(new_table_lines)
        return new_table_txt
