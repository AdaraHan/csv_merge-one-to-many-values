from flask import Flask, request, render_template, redirect, url_for, send_file
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    file_a = request.files['fileA']
    file_b = request.files['fileB']

    if file_a and file_b:
        file_a_path = os.path.join(app.config['UPLOAD_FOLDER'], file_a.filename)
        file_b_path = os.path.join(app.config['UPLOAD_FOLDER'], file_b.filename)
        file_a.save(file_a_path)
        file_b.save(file_b_path)

        dfA = pd.read_csv(file_a_path)
        dfB = pd.read_csv(file_b_path)

        columns_a = dfA.columns.tolist()
        columns_b = dfB.columns.tolist()

        return render_template('select_columns.html', columns_a=columns_a, columns_b=columns_b, file_a=file_a.filename,
                               file_b=file_b.filename)
    else:
        return redirect(url_for('index'))


@app.route('/process', methods=['POST'])
def process_files():
    file_a = request.form['file_a']
    file_b = request.form['file_b']
    column_a = request.form['column_a']
    column_b = request.form['column_b']
    selected_columns = request.form.getlist('selected_columns')

    file_a_path = os.path.join(app.config['UPLOAD_FOLDER'], file_a)
    file_b_path = os.path.join(app.config['UPLOAD_FOLDER'], file_b)

    dfA = pd.read_csv(file_a_path)
    dfB = pd.read_csv(file_b_path)

    merged_df = pd.merge(dfA, dfB[['authorName'] + selected_columns], left_on=column_a, right_on=column_b, how='left')

    output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_output.csv')
    merged_df.to_csv(output_file, index=False，encoding='utf-8-sig')

    return send_file(output_file, as_attachment=True, download_name='merged_output.csv')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
