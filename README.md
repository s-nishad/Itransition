Your SSH key is still not being recognized by GitHub. Let's systematically fix it:

---

## **1. Verify Your SSH Key Exists**
Check if your SSH key exists:

```bash
ls -al ~/.ssh
```

If you **don't** see `id_ed25519.pub` (or `id_rsa.pub`), generate a new key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
(For older systems: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`)

Press **Enter** to save it to the default location (`~/.ssh/id_ed25519`).

---

## **2. Add Your SSH Key to the Agent**
Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Then, add your key:

```bash
ssh-add ~/.ssh/id_ed25519
```
(For RSA: `ssh-add ~/.ssh/id_rsa`)

---

## **3. Add Your SSH Key to GitHub**
Get your **public key**:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output and **add it to GitHub**:

1. **Go to GitHub:** [SSH Keys Settings](https://github.com/settings/keys)
2. Click **"New SSH Key"**.
3. **Paste the key** and save.

---

## **4. Test SSH Connection to GitHub**
Run:

```bash
ssh -T git@github.com
```

Expected output:
```
Hi shohanur-is! You've successfully authenticated, but GitHub does not provide shell access.
```

If it still says **"Permission denied (publickey)"**, continue below.

---

## **5. Check Your SSH Remote URL**
Run:

```bash
git remote -v
```

If you see an **HTTPS URL** (e.g., `https://github.com/shohanur-is/bisqueUCSB3.git`), switch it to SSH:

```bash
git remote set-url origin git@github.com:shohanur-is/bisqueUCSB3.git
```

Now, retry:

```bash
git clone git@github.com:shohanur-is/bisqueUCSB3.git
```

---

## **6. Debug SSH Connection**
Run:

```bash
ssh -vT git@github.com
```

Look for **"debug1: Authentication succeeded"**. If it fails, your SSH key isn't being used. Make sure:

- Your key is added to the agent (`ssh-add -l`)
- The correct key is added to GitHub

---

## **7. Ensure SSH Config is Correct (Optional)**
Create or edit your SSH config:

```bash
nano ~/.ssh/config
```

Add the following:

```
Host github.com
    IdentityFile ~/.ssh/id_ed25519
    User git
```

Save and exit (`CTRL + X`, then `Y`, then Enter).

Now, restart the SSH agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

Try cloning again:

```bash
git clone git@github.com:shohanur-is/bisqueUCSB3.git
```

This should fix the issue. Let me know if you're still stuck! 🚀
