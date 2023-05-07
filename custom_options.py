from apache_beam.options.pipeline_options import PipelineOptions

class CustomOptions(PipelineOptions):
  """Arguments for the pipeline.
  """

  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_argument(
        "--project",
        help="The project where the Firestore repo resides."
        '"projects/<PROJECT_ID>".',
    )
    parser.add_argument(
        "--input_sub",
        help="The Cloud Pub/Sub subscription to read from."
        '"projects/<PROJECT_ID>/subscriptions/<SUBSCRIPTION_ID>".',
    )
    parser.add_argument(
        "--runner",
        default='DataflowRunner',
        help="Use DirectRunner (local) or DataflowRunner (GCP).",
    )
    parser.add_argument(
        "--streaming",
        default=True,
        help="Set to streaming.",
    )
    parser.add_argument(
        "--window_size_seconds",
        type=float,
        default=30.0,
        help="Pubsub reader window size in seconds.",
    )
    parser.add_argument(
        "--mode",
        default="GCP",
        help="GCP or local mode.",
    )

