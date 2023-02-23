# Tracking-COVID-19
This is just a page for family and friends to view COVID-19 numbers.

## Setup

Install [chruby][1], [ruby-install][2], and [direnv][3] via homebrew

> Note: `cd Tracking-COVID-19` refers to the main project directory for this
> repository.


```
brew install ruby-install direnv chruby
```

Install ruby 2.7.5:

```
ruby-install ruby 2.7.5
```

Open `~/.direnvrc` and paste this in it:

```sh
# Changes the current ruby version.
#
# Usage in .envrc:
#
#   use ruby [version]
#   PATH_add bin
use_ruby() {
  # load up chruby if needed and available
  if ! command -v chruby > /dev/null; then
    if [[ -f /usr/local/opt/chruby/share/chruby/chruby.sh ]]; then
      source /usr/local/opt/chruby/share/chruby/chruby.sh
    elif [[ -f /opt/homebrew/opt/chruby/share/chruby/chruby.sh ]]; then
      source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
    else
      >&2 echo "chruby not available! Run \`brew install chruby'"
      return 1
    fi
  fi

  # desired Ruby version as first parameter
  local ver="$1"

  # if version not given as parameter and there is a .ruby-version file, get
  # version from the file
  if [[ -z "$ver" ]] && [[ -f .ruby-version ]]; then
    ver=$(cat .ruby-version)
  fi

  # if the version still isn't set, error cause we don't know what to do
  if [[ -z "$ver" ]]; then
    >&2 echo "Unknown ruby version"
    return 1
  fi

  # switch to the desired ruby version
  chruby "$ver"
}
```

Enable direnv for this project

```
cd Tracking-COVID-19
direnv allow
```

Confirm it works:

```
cd Tracking-COVID-19
which ruby
```

Should output something like:

```
/Users/priddle/.rubies/ruby-2.7.5/bin/ruby
```

Install Jekyll:

```
cd Tracking-COVID-19
bundle install
bundle binstubs jekyll
```

Verify jekyll works:

```
cd Tracking-COVID-19
which jekyll
```

Should output something like:

```
/Users/priddle/Sites/tracking-covid-19.pasin3ru.github.io/bin/jekyll
```

Build the site:

```
jekyll build
```

[1]: https://github.com/postmodern/chruby
[2]: https://github.com/postmodern/ruby-install
[3]: https://github.com/direnv/direnv
