
export DJANGO_SETTINGS_MODULE="test_settings"

python3 -m coverage run -m django test polystorage
python3 -m coverage report --fail-under 100
