#!/bin/bash
show_spinner()
{
  local -r pid="${1}"
  local -r delay='0.75'
  local spinstr='\|/-'
  local temp
  while ps a | awk '{print $1}' | grep -q "${pid}"; do
    temp="${spinstr#?}"
    printf " [%c]  " "${spinstr}"
    spinstr=${temp}${spinstr%"${temp}"}
    sleep "${delay}"
    printf "\b\b\b\b\b\b"
  done
  printf "    \b\b\b\b"
}

if ! [ -d "/data/$1" ] || [ -z "$1" ] ; then
  echo "❌ Could not find data folder";
  echo "Usage: bash rad.sh data_folder";
  exit 1;
fi

echo "🤖 Installing dependencies...";
pip install -r /app/requirements.txt --root-user-action=ignore --progress-bar on | grep -v 'already satisfied' & show_spinner $!
pip install -e /app/rad --root-user-action=ignore --progress-bar on | grep -v 'already satisfied' & show_spinner $!

echo "📈 Running analysis...";
python main.py -p "/data/$1"