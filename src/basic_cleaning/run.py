#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    # Downloading dataframe
    logger.info("Downloading the dataframe")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    # Creating the dataframe
    logger.info("Reading the dataframe")
    dataframe = pd.read_csv(artifact_local_path)

    # Dropping outliers from price
    logger.info("Dropping outliers from Price")
    idx = dataframe['price'].between(args.min_price, args.max_price)
    dataframe = dataframe[idx].copy()

    # Dropping outliers from longitude and latitude
    logger.info("Dropping outliers from longitude and latitude")
    idx = dataframe['longitude'].between(-74.25, -73.50) & dataframe['latitude'].between(40.5, 41.2)
    dataframe = dataframe[idx].copy()

    # Processing last_review
    logger.info("Change last_review objet type to datetime")
    dataframe["last_review"] = pd.to_datetime(dataframe["last_review"])

    # Saving dataframe
    logger.info(f"Saving dataframe to {args.output_artifact}")
    dataframe.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file(args.output_artifact)

    logger.info("Logging artifact")
    run.log_artifact(artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Name fo the input artifact",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Name of the output artifact",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Artifact type",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help="Artifact description",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help="Minimum limit price",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help="Maximum limit price",## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
