import pickle

import numpy as np
import pandas as pd


def read_results(path):
    with open(path, "rb") as f:
        results = pickle.load(f)

    cols = ["loss", "loss_var", *results[0]["misc"]["vals"].keys()]
    res_df = pd.DataFrame(columns=cols)
    for i, res in enumerate(results):
        vals = res['misc']['vals']
        res_df.loc[i] = pd.Series({
            "loss": res['result']['loss'],
            "loss_var": res['result']['loss_variance'],
            **{key: (vals[key][0] if len(vals[key]) == 1 else 0) for key in vals}}
        )

    return res_df


def linplot(df: pd.DataFrame, col: str):
    """ # Todo documentation

    Args:
        df:
        col:

    Returns:

    """

    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    plt.scatter(df[col], df["loss"])

    model = LinearRegression().fit(df[col].values.reshape(-1, 1), df["loss"])
    x_line = np.linspace(df[col].min(), df[col].max(), 10).reshape(-1, 1)
    y_pred = model.predict(x_line)
    plt.plot(x_line, y_pred)
    plt.xlabel(col)
    plt.ylabel("loss")
