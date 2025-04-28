import matplotlib
matplotlib.use('Agg')

import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from flask import Flask, request, render_template, redirect, url_for
import seaborn as sns

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) < 2:
        return "Нужно минимум 2 числовых столбца!"

    X = df[[numeric_cols[0]]]
    y = df[numeric_cols[1]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    plt.scatter(X_test, y_test, label='Факт')
    plt.plot(X_test, preds, color='red', label='Прогноз')
    plt.legend()
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()

    return render_template('result.html', mse=round(mse, 2), plot_url=plot_path)


@app.route('/preview', methods=['POST'])
def preview_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    df.to_csv('last_upload.csv', index=False)

    columns = df.select_dtypes(include='number').columns.tolist()
    preview_html = df.head().to_html(classes='table table-bordered', index=False)

    return render_template('choose_columns.html', columns=columns, preview_table=preview_html)


@app.route('/train', methods=['POST'])
def train_model():
    df = pd.read_csv('last_upload.csv')
    x_col = request.form['x_column']
    y_col = request.form['y_column']

    df = df.dropna(subset=[x_col, y_col])

    df = df[(df[x_col] > 0) & (df[y_col] > 0)]

    x_max = df[x_col].quantile(0.99)
    y_max = df[y_col].quantile(0.99)
    df = df[(df[x_col] <= x_max) & (df[y_col] <= y_max)]

    X = df[[x_col]]
    y = df[y_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    plt.figure(figsize=(10, 6))
    plt.scatter(X_test, y_test, label='Факт', s=10, alpha=0.4)
    plt.plot(X_test, preds, color='red', label='Прогноз', linewidth=2)
    plt.xlabel(x_col, fontsize=14)
    plt.ylabel(y_col, fontsize=14)
    plt.title('Модель: линейная регрессия', fontsize=16)
    plt.legend(loc='upper left')
    plt.grid(True)
    plot_path = os.path.join(STATIC_FOLDER, 'plot.png')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(10, 8))
    sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, fmt='.2f', cmap='coolwarm')
    corr_path = os.path.join(STATIC_FOLDER, 'correlation.png')
    plt.savefig(corr_path)
    plt.close()

    return render_template('result.html', mse=round(mse, 2), plot_url=plot_path, corr_url=corr_path)


@app.route('/success', methods=['GET'])
def upload_success():
    return "Файл успешно загружен и обработан!"


if __name__ == '__main__':
    app.run(debug=True)
