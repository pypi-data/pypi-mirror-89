import pandas as pd
class chunk_manipulate():
    def __init__(self, df):
        self.df = df

    def chunk(self, c_start, c_end):
        """
        Creates a 'chunk' of rows from a dataframe

        ARGS: c_start - start index of desired section
              c_end - end index of desired section (not inclusive)

        returns: A section of rows between c_start and c_end

        """

        if c_start >= c_end:
            raise ValueError('c_end must be greater than c_start')
        else:
            self.df_chunk = self.df.iloc[(c_start):(c_end), :].copy()
        return self.df_chunk

    def row_insert(self, new_rows, split_index=0):
        """
            Inserts rows with indentical columns into a DataFrame

            ARGS: df - Dataframe for rows to be inserted into
                  new_rows - Dataframe with same columns as original DataFrame
                  split_index - index where data will be inputted, default 0

            returns: orignal DataFrame with inserted rows, index is reset.
        """

        if split_index == 0:
            self.df = pd.concat([new_rows, self.df]).reset_index(drop=True)
        elif split_index <0:
            raise ValueError('split_end must be integer of 0 or greater')
        else:
            df_split_1 = self.df.iloc[:(split_index), :].copy()
            df_split_2 = self.df.iloc[(split_index):, :].copy()
            self.df = pd.concat([df_split_1, new_rows, \
            df_split_2]).reset_index(drop=True)
        return self.df

    def multiply_rows(self, c_start, c_end, split_index):
        """
            Copies rows and pastes them back into its DataFrame at index

            ARGS: c_start - start index of desired section
                  c_end - end index of desired section (not inclusive)
                  split_index - index where data will be pasted, default 0

            returns: duplicates DataFrame rows, index is reset.
        """

        self.df = (self.row_insert(new_chunk.chunk(c_start,c_end),\
                 split_index))

        return self.df
