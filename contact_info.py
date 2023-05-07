from apache_beam import DoFn
import logging
import json

class ExtractContactInfo(DoFn):
    def process(self, element):
        """Extracts contact info from a person or patient resource
        """
        contactInfo = {}
        contactInfo['id'] = 'Unknown'
        msg = json.loads(element.data.decode("utf-8"))

        try:
            # Identifiers (https://www.hl7.org/fhir/patient-definitions.html#Patient.identifier)
            if 'identifier' in msg:
                # Just for this example, using the first identifier as the id
                contactInfo['id'] = msg['identifier'][0]['value']
                
                identifiers = {}
                for identifier in msg['identifier']:
                    system = identifier['system']
                    value = identifier['value']
                    identifiers[system] = value
                contactInfo['identifiers'] = identifiers

            # Name (https://www.hl7.org/fhir/patient-definitions.html#Patient.name)
            if 'name' in msg:
                for name in msg['name']:
                    use = name['use']
                    if use == 'official':
                        contactInfo['legalLastName'] = name['family']
                        if 'given' in name:
                            contactInfo['legalFirstName'] = name['given'][0]
                            if (len(name['given']) > 1):
                                contactInfo['legalMiddleName'] = name['given'][1]

            # Email (https://www.hl7.org/fhir/patient-definitions.html#Patient.telecom)
            if 'telecom' in msg:
                for telecom in msg['telecom']:
                    if telecom['system'] == 'email':
                        contactInfo['email'] = telecom['value']
                        break

            # Phones (https://www.hl7.org/fhir/patient-definitions.html#Patient.telecom)
            if 'telecom' in msg:
                for telecom in msg['telecom']:
                    if telecom['system'] == 'phone':
                        use = telecom['use']
                        if use == 'home':
                            contactInfo['phoneHome'] = telecom['value']
                        elif use == 'mobile':
                            contactInfo['phoneMobile'] = telecom['value']
                        elif use == 'work':
                            contactInfo['phoneWork'] = telecom['value']
            
            
        except Exception as e:
            logging.exception(f'ExtractContactInfo: {str(e)}')
        
        yield contactInfo