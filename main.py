import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from apache_beam import io, ParDo, Pipeline

import logging
import sys
import json

from contact_info import ExtractContactInfo
from custom_options import CustomOptions
from log_incoming import LogIncoming
from save_to_firestore import Save

payloadTypes = ['NameOnly','FullResource', 'UnknownPayload']

def partition_payload_type(payload, len):
    if payload is None:
        return payloadTypes.index('UnknownPayload')
    
    try:
        payloadType = payload.attributes.get("payloadType")
        if payloadType in payloadTypes:
            return payloadTypes.index(payloadType)
        else:
            return payloadTypes.index('UnknownPayload')
    except Exception as e:
        logging.exception(f'partition_payload_type: {str(e)}!')
        return payloadTypes.index('UnknownPayload')


resourceTypes = ['Person', 'OtherResourceType']
def partition_resource_type(payload, len):
    if payload is None:
        return resourceTypes.index('OtherResourceType')

    try:
        data = json.loads(payload.data)
        resourceType = 'OtherResourceType'
        if "resourceType" in data:
            resourceType = data["resourceType"]

        return resourceTypes.index(resourceType)
    except Exception as e:
        logging.exception(f'partition_resource_type: {str(e)}!')
        return resourceTypes.index('OtherResourceType')
    
def runPipeline(pipeline_options: CustomOptions):
    with Pipeline(options=pipeline_options) as pipeline:
        sub = pipeline_options.input_sub

        NameOnly, FullResource, UnknownPayload = (
            pipeline
            | "Read from Pub/Sub" >> io.ReadFromPubSub(subscription=sub, with_attributes=True)
            | "Log the message" >> beam.ParDo(LogIncoming())
            | "Partition by payloadType" >> beam.Partition(partition_payload_type, len(payloadTypes))
        )

        nameOnlyLookup = (
                # Look these up by id in the Healthcare API
                NameOnly | 'TODO: lookup name only payload types' >>  beam.Map(lambda x: logging.debug(f'NameOnlyLookup {x}'))
        )

        UnknownPayloadLog =  (
            UnknownPayload 
            | 'Log unrecognized payload types' >> beam.Map(lambda x: logging.warn(f'Unrecognized payload type {x}'))
        ) 

        ContactInfoProcess = (
            FullResource | 'Filter by Person' >> beam.Filter(lambda x: partition_resource_type(x, len(resourceTypes)) == resourceTypes.index('Person'))
                         | 'Extract contact info' >> beam.ParDo(ExtractContactInfo())
                         | 'Save to Firestore' >> beam.ParDo(Save(), pipeline_options)
        )           

if __name__=='__main__':
    try:
        options=PipelineOptions(sys.argv)
        
        # Set `save_main_session` to True so DoFns can access globally imported modules.
        options.view_as(SetupOptions).save_main_session = True
        pipeline_options = options.view_as(CustomOptions)

        # Clear any other logging configs
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Configure Logging
        if (pipeline_options.mode == 'local'):
            logging.basicConfig(
                format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', 
                level=logging.INFO, 
                filename='log.txt', 
                filemode='w') # 'w' to overwrite, 'a' to append
        else:
            logging.basicConfig(
                format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', 
                level=logging.INFO)
            
        logging.info(f'Pipeline options: {pipeline_options}')

        runPipeline(pipeline_options)
    except Exception as e:
        logging.exception(f'Global exception: {str(e)}!')
        logging.shutdown()