from apache_beam import DoFn
from google.cloud import firestore
import logging

from custom_options import CustomOptions

class Save(DoFn):
    def process(self, element, custom_options: CustomOptions):
        """Saves contact to Firestore
        """
        try:
            project = custom_options.get_all_options()['project']
            collection = 'ContactInfo'
            id = element['id']

            db = firestore.Client(project)
            # Upsert the contact info - merge=True to maintain older fields
            db.collection(collection).document(id).set(element, merge=True)

            logging.info(f'Updated contact info for {id}')

        except Exception as e:
            logging.exception(f'Save: {str(e)}')

        yield element