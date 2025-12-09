## Webhook Research Summary: VCS Integration 

### Webhook Documentation Sources and Core Data

#### GitHub (Docs: "Webhook events and payloads")

* **Key Identity Fields:**
    * `author.email`
    * `sender.login` (GitHub username of the pusher)
    * `commit id`
* **Security Header:** `X-Hub-Signature-256: sha256=<hmac>` (Requires HMAC SHA-256 verification).
* **Payload Contents (`Push` Event):**
    * `pusher`: Information on the user who initiated the push.
    * `commits[]`: An array detailing all commits in the push.
        * `id` (SHA)
        * `message`
        * `timestamp`
        * `author` (name and email)
        * `committer`
        * Lists of `added`, `removed`, and `modified` files.

#### GitLab (Docs: "Webhooks / System Hooks")

* **Key Identity Fields:**
    * `user_email` (Email of the pusher)
    * `user_username` (Username of the pusher)
    * `commit author email`
* **Security Header:** `X-Gitlab-Token` (Requires direct token matching verification).
* **Payload Contents (`Push` Event):**
    * `user_username`, `user_email`: Details of the user who triggered the webhook.
    * `commits[]`: Array of commits.
        * `id` (SHA)
        * `message`
        * `timestamp`
        * `author.email`
        * `added`, `modified`, `removed` file lists.

#### Bitbucket (Docs: "Bitbucket Cloud Webhooks")

* **Key Identity Fields:**
    * `actor.username` (Username of the pusher)
    * `commit author email` (Found within `author.raw`)
* **Security Header:** `X-Hub-Signature` (Requires HMAC SHA-256 verification).
* **Payload Contents (`Repo Push` Event):**
    * `actor`: Details on the user who performed the push.
    * `push.changes[].commits[]`: Array of commits linked to the change.
        * `hash` (SHA)
        * `message`
        * `author.raw` (Contains name and email)
        * `date`

---

###  Strategies for Mapping Commits $\rightarrow$ Users

I identified four primary methods forus to reliably link the commit data to internal user profiles:

* **Method 1: Match by Email (Recommended Primary)**
    * **Source:** `commit.author.email` (Available across all platforms).
    * **Flow:** Match `commit.author.email` $\rightarrow$ `user\_profile.email` $\rightarrow$ `user\_id`.
    * **Note:** We must account for users using platform-generated "no-reply" emails (e.g., GitHub).

* **Method 2: Match by Git Platform Username**
    * **Source:** GitHub (`sender.login`), GitLab (`user_username`), Bitbucket (`actor.username`).
    * **Flow:** Match `platform_username` $\rightarrow$ `saved\_user.platform\_username`.
    * **Use Case:** Ideal for commits where the email is hidden or a no-reply address. Requires the user to link their account with us.

* **Method 3: Match by Committer Identity**
    * **Source:** `committer` fields (Available in payload).
    * **Purpose:** Useful for detecting scenarios where the author and committer are different (e.g., pair programming, automated merges, or bot actions).

* **Method 4: Use OAuth Integration (Most Reliable)**
    * **Process:** We use the VCS (GitHub, GitLab, etc.) for user login to obtain and store a verified email and username link.
    * **Result:** Provides a guaranteed mapping between our internal user ID and the external platform identity.

---

###Security Requirements and Best Practices

Security must be our top priority. I have documented the specific verification steps we must follow:

#### Signature/Token Verification (The Mandate)

| Platform | Verification Requirement | Implementation Steps (For Me) |
| :--- | :--- | :--- |
| **GitHub** | HMAC SHA-256 Signature | we must recalculate the hash of the raw payload using our stored secret and compare it byte-for-byte with the value in the `X-Hub-Signature-256` header. |
| **GitLab** | Token Match | we must verify that the content of the `X-Gitlab-Token` header exactly matches the secret token we configured. |
| **Bitbucket** | HMAC SHA-256 Signature | I must implement the same HMAC SHA-256 signature recalculation and comparison as GitHub, using the `X-Hub-Signature` header. |

#### General Best Practices (For Our Endpoint)

* **Transmission Security:** I will ensure our webhook endpoint uses **HTTPS** to encrypt all data in transit.
* **Input Validation:**
    * Only accept `POST` requests.
    * Validate the `Content-Type` is `application/json`.
* **Replay Attack Protection:** If timestamps are available in headers, I will reject requests older than a short window (e.g., 5 minutes).
* **Logging & Monitoring:** I will ensure we securely log all signature mismatch attempts for security auditing.
* **Data Handling:I must ensure we store sensitive data (like commit emails) securely and in compliance with our data policies.

##  Conclusion: Webhook Integration Readiness

Based on my detailed research, I conclude that we have all the necessary information to successfully implement robust and secure webhook handlers for GitHub, GitLab, and Bitbucket.

**The core findings ensure we are ready to proceed with implementation:**

* **Data Consistency:** The critical data required to map commits to users—specifically the **author email** and **commit ID**—is consistently available across all three VCS payloads, allowing us to build a standardized processing pipeline.
* **Security Strategy Defined:** I have defined the platform-specific security requirements. We must prioritize payload validation using **HMAC SHA-256 signatures** for GitHub and Bitbucket, and **token matching** for GitLab, all secured over **HTTPS**.
* **User Mapping Plan:** I have established a clear, multi-method strategy for mapping commits to internal user profiles, primarily relying on the **commit author email** as the most reliable identifier.

Our next step should be moving from research to development by designing the specific API endpoint that will handle the payload reception and verification as defined here.

