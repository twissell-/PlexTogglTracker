# Rin

`rin` is my automated solution for tracking to [Toggl](https://toggl.com) the time spent watching stuff on [Plex](https://www.plex.tv). Time-tracking is very personal, everyone has its own way of doing it, so feel free to adapt this code to fit your needs.

## How does it work?

`rui` is a [Flask](https://github.com/pallets/flask) application. It serves an endpoint that must be added to your Plex account webhooks.

When a `media.play` or `media.resume` event is received from Plex, `rin` creates a Toggl time entry and stops it when receives a `media.pause` or `media.stop` event.

The description of the time entry is always the title of what is being played. The project depends on the configuration. `rin` maps Plex libraries to Toggl projects. (See [mapping](#mapping)).

## Basic Usage

### Installation

Clone the repository:
```sh
git clone git@github.com:twissell-/rin.git
```

Create and install dependencies:
```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Configuration File

Create a new configuration file from the template:
```sh
cp config-template.json config.json
```

Open it and fill in the values

#### endpoint
The endpoint for the webhook. I recommend to generate a random hash.

On linux you can use:
```sh
echo $RANDOM | md5sum | head -c32
```

#### toggl_api_token
You can find it under "My Profile" in your Toggl account. You can also put your api token on a `TOGGL_API_TOKEN` environment variable. The later takes precedence over the former.

#### plex_username
As it appears on you Plex profile. This is used to filter out events not
generated by you.

#### mapping
A list of objects telling `rin` what project assign to the created time entry based on in which library the file you are playing is.

```json
"mapping": [
  {
    "libraries": ["TV Shows"],
    "project": "Watching TV"
  }
```
This config will track shows on the "TV Shows" Plex library on the "Watching TV" project.

> **Note:** Media on libraries not defined here or assigned to a nonexistent project will be ignored.

### Run the local server

```
python run.sh
```

## Advance Usage

`rin` can be deployed as any other Flask application. Check [its documentation](https://flask.palletsprojects.com/en/2.3.x/deploying/) for more information.

## Limitations

- Only working for `movies` and `episode` Plex types.