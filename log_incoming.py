from apache_beam import DoFn
import logging

class LogIncoming(DoFn):
    def process(self, element):
        """ Logs incoming message and returns element
        """
        
        try:            
            logging.debug(f'Processing message {str(element)}')
        except Exception as e:
            logging.exception(f'LogMpiid: {str(e)}')

        yield element