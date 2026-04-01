# Publishing BizLens to PyPI 📦

This guide walks you through publishing your package to PyPI (Python Package Index).

---

## ⚠️ Pre-Flight Checklist

Before you publish, ensure:

- [ ] All validation steps in [VALIDATION.md](VALIDATION.md) are complete
- [ ] Version number in `pyproject.toml` is correct (currently `0.5.0`)
- [ ] `README.md` is polished and complete
- [ ] `LICENSE` file is present
- [ ] `.gitignore` is properly configured
- [ ] No sensitive data in `__init__.py`, `core.py`, or config files
- [ ] PyPI account created at https://pypi.org/account/register/

---

## Step 1: Create PyPI Account

1. Go to **https://pypi.org/account/register/**
2. Create your account
3. Verify your email address
4. **Save your username and password** (you won't need password for uploads—use API tokens instead)

---

## Step 2: Generate API Token

⚠️ **This is the secure way to upload (passwords are deprecated)**

1. Log into **https://pypi.org/**
2. Click your **Profile** (top right)
3. Select **Account Settings** → **API tokens**
4. Click **Add API token**
5. Name it: `bizlens-upload`
6. Scope: **Entire Account** (for first upload)
7. Click **Create token**
8. **Copy the entire token immediately** — you won't see it again!

Token format: `pypi-AgEIcHlwaS5vcmc...` (very long string)

**Save it somewhere secure** (you'll use it in Step 4)

---

## Step 3: Build Distribution Packages

From the **root** `bizlens/` folder:

```bash
# Ensure build and twine are installed
pip install --upgrade build twine

# Build distributions
python -m build
```

✅ **Verify**: You should see:
```bash
ls -lh dist/
# bizlens-0.5.0-py3-none-any.whl    (~150 KB)
# bizlens-0.5.0.tar.gz              (~100 KB)
```

---

## Step 4a: Upload to PyPI (Interactive)

```bash
twine upload dist/*
```

When prompted:
- **Username**: `__token__` (literally, not your username)
- **Password**: Paste your API token from Step 2

Example:
```
Uploading distributions to https://pypi.org/legacy/
Enter your username: __token__
Enter your password: pypi-AgEIcHlwaS5vcmc...

Uploading bizlens-0.5.0-py3-none-any.whl
Uploading bizlens-0.5.0.tar.gz
100%|████████████| 2/2 [00:05<00:00, 2.50s/it]

View at:
https://pypi.org/project/bizlens/
```

---

## Step 4b: Upload to PyPI (Automated with .pypirc)

For repeated uploads, save credentials in `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

Then upload:
```bash
twine upload dist/*
```

**⚠️ Warning**: Store `.pypirc` safely; it contains your API token!

---

## Step 5: Verify Upload

After a successful upload (usually 1-2 minutes), check:

1. **PyPI Package Page**: https://pypi.org/project/bizlens/
2. **Files Tab**: Should show `.whl` and `.tar.gz`
3. **Version History**: Should list `0.5.0`

---

## Step 6: Install from PyPI (Test It!)

From a different terminal or virtual environment:

```bash
pip install bizlens
```

Then test:
```bash
python -c "import bizlens as bl; print(bl.__version__)"
# Output: 0.5.0
```

---

## Step 7: Update Version for Next Release

When you're ready for version 0.6.0:

1. Update `pyproject.toml`:
   ```toml
   version = "0.6.0"
   ```

2. Update `src/bizlens/__init__.py`:
   ```python
   __version__ = "0.6.0"
   ```

3. Rebuild and re-upload:
   ```bash
   python -m build
   twine upload dist/*
   ```

---

## 🎉 Success Indicators

You'll know it worked when:

✅ Package appears on https://pypi.org/project/bizlens/
✅ `pip install bizlens` works from any environment
✅ GitHub shows a PyPI badge
✅ Docs are visible on PyPI

---

## Troubleshooting

### "Invalid or expired API token"

- Regenerate a new token at https://pypi.org/account/
- Make sure you copied the **entire** token
- Check for trailing spaces in your password

### "Package 'bizlens' already registered"

- This is expected on re-uploads (different version)
- The version number in `pyproject.toml` must be **unique**

### "File already exists"

- Delete `dist/` folder and rebuild:
  ```bash
  rm -rf dist/
  python -m build
  ```

### "403 Forbidden"

- Your API token may have expired or been revoked
- Create a new token at https://pypi.org/account/

### "404 Not Found"

- You're uploading to the wrong URL
- Ensure using `twine` (not `pip`)
- Check `~/.pypirc` has correct server URL

---

## Security Best Practices

🔒 **Do:**
- Use API tokens, not passwords
- Regenerate tokens periodically
- Store `.pypirc` with restricted permissions: `chmod 600 ~/.pypirc`
- Use environment variable instead of `.pypirc`:
  ```bash
  export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...
  twine upload dist/*
  ```

🚫 **Don't:**
- Share your API token in public repositories
- Commit `.pypirc` to Git
- Use your PyPI password for `twine` (use tokens only)
- Include API tokens in issue tracker or emails

---

## Next Steps

Once published:

1. **Announce on social media/forums**
   - Tweet: "🎉 BizLens 0.5.0 is live on PyPI!"
   - Post on Reddit, Dev.to, etc.

2. **Create GitHub Releases**
   ```bash
   git tag -a v0.5.0 -m "BizLens 0.5.0"
   git push origin v0.5.0
   ```

3. **Set Up CI/CD** (optional)
   - Auto-publish on GitHub tag
   - GitHub Actions + PyPI

4. **Monitor Downloads**
   - Check PyPI stats: https://pypi.org/project/bizlens/
   - Track: https://libraries.io/pypi/bizlens

---

## Helpful Links

| Link | Purpose |
|------|---------|
| https://pypi.org/ | Official PyPI |
| https://test.pypi.org/ | Test PyPI (practice uploads) |
| https://twine.readthedocs.io/ | Twine docs |
| https://packaging.python.org/ | Python packaging guide |

---

## 🎓 For Educators/Students

If you're teaching package distribution:

1. **First publish to TestPyPI**: https://test.pypi.org/
   ```bash
   twine upload --repository testpypi dist/*
   ```

2. **Then move to real PyPI** after validation

3. **Show students the package page** to demonstrate professional software distribution

---

**Congratulations on publishing BizLens! 🚀**
