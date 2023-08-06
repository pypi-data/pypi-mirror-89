from setuptools import setup, find_packages

plist = find_packages('src')
print(plist)

setup(
    name='libpyka',
    version='0.0.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # 作者・プロジェクト情報
    author='kentarou arakawa',
    author_email='kagalpan+pypi@kacpp.xyz',
    # プロジェクトのホームページのURL
    url='http://example.com/',

    # 短い説明文と長い説明文を用意
    # content_typeは下記のいずれか
    #   text/plain, text/x-rst, text/markdown
    description='Pythonの一般的ユーティリティーライブラリ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    #pythonのバージョンは3.6以上で4未満
    python_requires='~=3.6',

    #PyPI上で検索閲覧される情報
    # OS, ライセンス, Pythonバージョン
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],

    # 依存するパッケージ
    # 1.x以上のパッケージをインストールする場合 ==1.*
    # 1.3以上で1.xの最新版をインストールする場合 >=1.3 ~=1.3
    install_requires=[
        'requests>=2.*',
        'psycopg2>=2.*'
    ],

    # *.py以外のデーターファイルを含める
    # package_data = {'パッケージ名': ['データーファイルのパス']}
    # データーファイルのパスは相対パス
    package_data={'libpyka': ['conf/*']}
)



