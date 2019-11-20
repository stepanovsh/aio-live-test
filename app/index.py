import re


class DocumentAppearance:
    """In memory service class to detect word appearances in the DB """
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


class DocumentDB:
    """
    In memory database representing the already indexed documents.
    """

    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    @property
    def indexed(self):
        return bool(self.index)

    def index_document(self, document):

        # Remove punctuation from the text.
        clean_text = re.sub(r'[^\w\s]', '', document['text'])
        terms = clean_text.split(' ')
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term = term.lower()
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = DocumentAppearance(document['id'], term_frequency + 1)

        # Update the inverted index
        update_dict = {key: [appearance] if key not in self.index else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances.
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        return {term.lower(): self.index[term.lower()] for term in query.split(' ') if term.lower() in self.index}


db = DocumentDB()
index = InvertedIndex(db)


def indexing_document(games_result):
    for game_id, name in games_result.values():
        document = {
            'id': str(game_id),
            'text': str(name)
        }
        index.index_document(document)
