# Contributing to Drivux

Thanks for your interest in improving Drivux!

## Reporting bugs

Open an [issue](https://github.com/RaphGod/drivux/issues) with:
- What happened vs what you expected
- Your Linux distro and desktop environment (KDE, GNOME, etc.)
- The error message or screenshot if possible

## Suggesting features

Open an [issue](https://github.com/RaphGod/drivux/issues) with the label `enhancement` and describe what you'd like to see.

## Contributing code

1. **Fork** the repo and clone your fork
2. Create a branch: `git checkout -b my-feature`
3. Make your changes
4. Test locally: `python -m drivux.main`
5. Commit and push to your fork
6. Open a **Pull Request** against `main`

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/drivux.git
cd drivux
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Guidelines

- Keep it simple - small focused PRs are easier to review
- Follow the existing code style
- Test your changes on your machine before submitting
- If adding UI text, add translations in `drivux/i18n.py` (at least `en` and `fr`, other languages are welcome)

### Adding a new language

Edit `drivux/i18n.py` and add your language dict in `TRANSLATIONS`. Copy the `en` dict as a template. The app auto-detects the system locale.

## Questions?

Open an issue, we'll be happy to help.
