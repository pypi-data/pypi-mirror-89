# autoregressor

You can install autoregressor from PyPI
    
    $ pip install autoregressor
    
Once the library is installed, import the modules in your python notebook or any IDE of your choice.

    $ import autoregreessor
    from autoregressor import compute
    
We now have the package imported. To use the library, we use:

    prediction = autoregressor(X_train , y_train , X_test)
    
Where, 

* prediction - Predicted output of the Regression model.
* X_train - Training dataset
* y_train - Target variable of the training dataset
*X_test - Testing dataset