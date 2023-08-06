from NASA import session
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URL
GENELAB_URL = "https://genelab-data.ndc.nasa.gov/genelab/data/"

# ENDPOINTS
DATA_QUERY_ENDPOINT = "glds/files/"
DATA_SEARCH_ENDPOINT = "search"
METADATA_QUERY_ENDPOINT = "glds/meta/"

DEFAULT_DB_TYPE = "cgene"
DEFAULT_PAGE = 0
DEFAULT_SIZE = 25
DEFAULT_SORTING = "Accession"
DEFAULT_ORDER = "ASC"
DEFAULT_STUDY_ID = 99


class GENELAB(object):
    """
    GENELAB

    NASA GeneLab provides a RESTful Application Programming Interfaces (API)
    to its full-text search, and data and metadata retrieval capabilities.
    The GeneLab Data Query API returns metadata on data files associated with
    dataset(s), including the location of these files for download.\n
    The GeneLabMetadata Query API returns entire sets of metadata for input
    dataset accession numbers. TheGeneLab Dataset Search API can be used to
    search dataset metadata by keywords and/or metadata. It can also be used
    to provide search of three other omics databases:
    - The National Institutes of Health (NIH) National Center for
        Biotechnology Information's (NCBI) GeneExpression Omnibus (GEO)\n
    - The European Bioinformatics Institute's (EBI) Proteomics Identification
        (PRIDE)\n
    - The Argonne National Laboratory's (ANL) Metagenomics Rapid Annotations
        using Subsystems Technology (MG-RAST).\n

    """

    @staticmethod
    def get_all_studies(with_ids=DEFAULT_STUDY_ID,
                        page=DEFAULT_PAGE,
                        size=DEFAULT_SIZE):
        """
        All studies
        """
        session.params.clear()
        session.params['page'] = page
        session.params['size'] = size
        all_studies_url = f"{GENELAB_URL}{DATA_QUERY_ENDPOINT}{with_ids}"
        try:
            response = session.get(all_studies_url)
            return response.json()
        except Exception as e:
            logger.error(f'Studies unavailable because: {e}')

    @staticmethod
    def get_metadata_for_study(accession_number=DEFAULT_STUDY_ID):
        """
        Get metadata for single GLDS accession number
        """
        session.params.clear()
        metadata_url = f"{GENELAB_URL}{METADATA_QUERY_ENDPOINT}\
                            {accession_number}"
        try:
            response = session.get(metadata_url)
            return response.json()
        except Exception as e:
            logger.error(f'Metadata unavailable because: {e}')

    @staticmethod
    def search(term=None,
                from=DEFAULT_PAGE,
                size=DEFAULT_SIZE,
                source_type=DEFAULT_DB_TYPE,
                sorted_by=DEFAULT_SORTING,
                ordered_by=DEFAULT_ORDER,
                filter_field=None,
                filter_value=None):
        """
        Search

        :param: term - search keyword
        :param: from - starting page
        :param: size - search result display count
        :param: type - datasource: cgene, nih_geo, nih_geo_gse, ebi_pride,
                                mg_rast (accepts comma separated values)
        :param: sort - sort field
        :param: order - sort order
        :return:
        """
        session.params.clear()
        session.params['term'] = term
        session.params['from'] = from
        session.params['size'] = size
        session.params['type'] = source_type
        session.params['sort'] = sorted_by
        session.params['order'] = ordered_by
        if filter_field and filter_value:
            session.params['ffield'] = filter_field
            session.params['fvalue'] = filter_value
        search_url = f"{GENELAB_URL}{DATA_SEARCH_ENDPOINT}"
        try:
            response = session.get(search_url)
            return response.json()
        except Exception as e:
            logger.error(f'Studies unavailable because: {e}')
