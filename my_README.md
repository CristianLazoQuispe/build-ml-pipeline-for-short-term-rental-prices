
# Running pipeline step by step


    $ mlflow run . -P steps=download 

    $ mlflow run src/eda

    $ mlflow run . -P steps=basic_cleaning

    $ mlflow run . -P steps=data_check


<img src="images/data_test_results.png?raw=true" width="800" height = "200"/>

    $ mlflow run . -P steps=data_split

    $ mlflow run . \
    -P steps=train_random_forest \
    -P hydra_options="modeling.random_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1 -m"


# best parameters model v8

Score: 0.5735808255359318
MAE: 32.78851749539595

        criterion : "mae"
        max_depth : 15
        max_features : 0.33
        max_tfidf_features : 10
        min_samples_leaf : 3
        min_samples_split : 4
        n_estimators : 100

Running test

    $ mlflow run . -P steps=test_regression_model

<img src="images/test_model.png?raw=true" width="1000" height = "200"/>


Train the model on a new data sample

    $ mlflow run https://github.com/CristianLazoQuispe/build-ml-pipeline-for-short-term-rental-prices.git \
                -v 1.0.0 \
                -P hydra_options="etl.sample='sample2.csv'"

<img src="images/sample_error_detected_in_test.png?raw=true" width="1000" height = "200"/>

Adding filters in basic_cleaning


        idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
        df = df[idx].copy()

Testing again

    $ mlflow run https://github.com/CristianLazoQuispe/build-ml-pipeline-for-short-term-rental-prices.git \
                -v 1.0.0 \
                -P hydra_options="etl.sample='sample2.csv'"
