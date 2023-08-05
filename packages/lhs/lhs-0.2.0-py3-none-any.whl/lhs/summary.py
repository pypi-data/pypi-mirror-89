import pypfilt


class LhsSamples(pypfilt.Table):
    def dtype(self, ctx, obs_list, name):
        self.__sampler = ctx.component['sampler']
        val_samples = self.__sampler.sample_values
        param_cols = [(param, values.dtype, values.shape[1:])
                      for param, values in val_samples.items()]
        return [('ix', int)] + param_cols

    def n_rows(self, start_date, end_date, n_days, n_sys, forecasting):
        return self.__sampler.num_samples

    def add_rows(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        pass

    def finished(self, hist, weights, fs_date, dates, obs_types, insert_fn):
        val_samples = self.__sampler.sample_values
        for ix in range(self.__sampler.num_samples):
            param_vals = [values[ix] for values in val_samples.values()]
            insert_fn((ix, *param_vals))
