
#
# .bashrc.override.sh
#

# persistent bash history
HISTFILE=~/.bash_history
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

# set some django env vars
source /entrypoint

# create superuser if it doesn't exist
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

if not User.objects.filter(phone="${DJANGO_SUPERUSER_PHONE}").exists():
    User.objects.create_superuser("${DJANGO_SUPERUSER_PHONE}", "${DJANGO_SUPERUSER_PASSWORD}")
    print("Superuser created.")
EOF

pre-commit install

# restore default shell options
set +o errexit
set +o pipefail
set +o nounset
