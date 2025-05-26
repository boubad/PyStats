""" module fixture """


from info import csvutils


class TestFixture(object):
    @property
    def db_url(self) -> str:
        return "http://boubad:bouba256@services.diarra.ovh:5984/"

    @property
    def db_name(self) -> str:
        return "dbtest"

    @property
    def csv_filepath(self) -> str:
        s = "./data/testindivs.csv"
        try:
            f = open(s)
            f.close()
        except OSError:
            s = "../data/testindivs.csv"
        return s

    @property
    def csv_filepath_full(self) -> str:
        s = "./data/notes_full.csv"
        try:
            f = open(s)
            f.close()
        except OSError:
            s = "../data/notes_full.csv"
        return s
    
    def read_csv(self) ->tuple[list[str], list[str], list[list[float]]]:
        return csvutils.read_csv(self.csv_filepath)
