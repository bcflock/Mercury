from mercury.app import Mercury
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Mercury",
        description="""
            A tool for creating data access
            lambdas specified using yaml
        """
    )
    parser.add_argument( 
        "--config",
        default="config.mercury.yml")
    parser.add_argument(
        "--template",
        default = "template"
    )
    parser.add_argument(
        '--output',
        default='.'
    )
    parser.add_argument(
        "--tab-width",
        default=2
    )

    args = parser.parse_args()
    Mercury(args.config, args.template, args.output).execute()