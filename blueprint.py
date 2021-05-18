from pandas.api.types import is_bool_dtype, is_numeric_dtype
from eda_report.validate import validate_univariate_input

class Variable:
    """This is the blueprint for containers to hold the contents and
    characteristics of *individual columns/features*.
    """

    def __init__(self, data, *, name=None):
        """Initialise an instance of :class:`Variable`.

        :param data: The data to process.
        :type data: ``pandas.Series``
        :param graph_color: The color to apply to the graphs created,
            defaults to 'orangered'.
        :type graph_color: str, optional
        :param name: The feature's name.
        :type name: str, optional
        """
        self.data = validate_univariate_input(data)
        #: The *name* of the *column/feature*. If unspecified in the ``name``
        #: argument during instantiation, this will be taken as the value of
        #: the ``name`` attribute of the input data.
        self.name = self._get_name(name)
        #: The *type* of feature; either *categorical* or *numeric*.
        self.var_type = self._get_variable_type()
        #: *Summary statistics* for the *column/feature*, as a
        #: ``pandas.DataFrame``.
        self.statistics = self._get_summary_statictics()
        #: The *number of unique values* present in the *column/feature*.
        self.num_unique = self.data.nunique()
        #: The set of *unique values* present in the *column/feature*.
        self.unique = set(self.data.unique())
        #: The number of *missing values* (``NaN``, ``None``, ``NA``, ...).
        self.missing = self._get_missing_values()
        #: Set types of graphs
        self.graph = self._graphs()
    
    def _get_name(self, name=None):
        """Set the feature's name.

        :param name: The name to give the feature, defaults to None
        :type name: str, optional
        """
        if name:
            self.data = self.data.rename(name)

        return self.data.name

    def _get_variable_type(self):
        """Get the variable type: 'categorical' or 'numeric'.
        """
        if is_numeric_dtype(self.data) and not is_bool_dtype(self.data):
            # Only int and float types
            return 'numeric'
        else:
            # Handle bool, string, datetime, etc as categorical
            self.data = self.data.astype('category')
            return 'categorical'

    def _get_summary_statictics(self):
        """Get summary statistics for the column/feature.
        """
        if self.var_type == 'numeric':
            return self._numeric_summary_statictics()
        elif self.var_type == 'categorical':
            return self._categorical_summary_statictics()

    def _numeric_summary_statictics(self):
        """Get summary statistics for a numeric column/feature.
        """
        summary = self.data.describe()
        summary.index = [
            'Number of observations', 'Average', 'Standard Deviation',
            'Minimum', 'Lower Quartile', 'Median', 'Upper Quartile', 'Maximum'
        ]
        summary['Skewness'] = self.data.skew()
        summary['Kurtosis'] = self.data.kurt()
        return summary.round(7).to_frame()

    def _categorical_summary_statictics(self):
        """Get summary statistics for a categorical column/feature.
        """
        summary = self.data.describe()[['count', 'unique', 'top']]
        summary.index = ['Number of observations', 'Unique values',
                         'Mode (Highest occurring value)']

        # Get most common items and their relative frequency (%)
        most_common_items = self.data.value_counts().head()
        n = len(self.data)
        var = most_common_items.index.to_list()
        count = most_common_items.values.tolist()
        percentage = most_common_items.apply(lambda x: f'{x / n:.2%}').values.tolist()
        self.most_common_items = \
            var, percentage, count

        return summary.to_frame()

    def _get_missing_values(self):
        """Get the number of missing values in the column/feature.
        """
        missing_values = self.data.isna().sum()
        if missing_values == 0:
            return None
        else:
            return missing_values, round(missing_values / len(self.data), 3)

    def _graphs(self):
        """Plot graphs for the column/feature, based on variable type.
        """
        if self.var_type == 'numeric':
            return ['hist_and_boxplot', 'prob_plot', 'run_plot']
        elif self.var_type == 'categorical':
            return ['bar_plot']


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('static/dataset/cars.csv', delimiter=',')
    sub_df = df[[' time-to-60', ' brand', ' year']]

    v = Variable(sub_df[' brand'])
    # print(v.missing)
    # print(v.unique)
    print(v.most_common_items)