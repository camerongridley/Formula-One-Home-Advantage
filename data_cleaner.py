class DataCleaner:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self):
        pass

    def remove_newline(self, df, num_replace_val=-1, obj_replace_val='None'):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to search for \N
        num_replace_val : int
            Number to replace newline with. Defaults to -1. 
        obj_replace_val : string
            String to replace newline with in oject dtype col

        Returns
        -------
        int
            Description of return value

        """
        
        # for col_name in df.columns:
        #     if df[col_name].dtype in ['int32', 'int64','float32', 'float64']:
        #         df[col_name].replace(r'\\N|\\n',  value=[replace_val, replace_val], regex=True, inplace=True)
        #     else:
        #         df[col_name].replace(r'\\N|\\n',  value=[str(replace_val), str(obj_replace_val)], regex=True, inplace=True)
        
        # for col_name in df_all.columns:
        #     if df_all[col_name].dtype in ['int32', 'int64','float32', 'float64']:
        #         df_all[col_name].replace(r'\\N',  replace_val, regex=True, inplace=True)
        #     else:
        #         df_all[col_name].replace(r'\\N',  str(obj_replace_val), regex=True, inplace=True)

        pass