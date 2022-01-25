function last {
    array=("${@}")
    last_index=$(( $# - 1 ))
    last_item=${array[$last_index]}
    echo "$last_item"
}
perl -pi -e 's/VERSION="[^"]+"/VERSION="'$(cat version.txt)'"/' setup.py
python setup.py sdist
files=$( ls dist/*.tar.gz | sort -V )
lastfile=$( last $files )
version=${lastfile##*-}
version=${version%.tar.gz}
echo $version
twine check "$lastfile"
twine upload --repository pypitest "$lastfile"
echo "Install at:"
echo "python -m pip install -i https://test.pypi.org/simple/ underscore3==$version"
sleep 15
# python -m pip install --upgrade --index-url https://test.pypi.org/simple/ underscore3
python -m pip install -i https://test.pypi.org/simple/ underscore3==$version
cmd /c "python -m pip install -i https://test.pypi.org/simple/ underscore3==$version"
