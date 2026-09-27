---
title: "Engineering Onboarding Runbook"
owner: "Manish Grover, Director - Engineering"
last_updated: 2026-03-16
version: 4.0
---

# Engineering Onboarding Runbook

For engineers joining a Nexora delivery team. Covers the first two weeks. The HR side of
onboarding is in the Onboarding and Training Manual (HR-MAN-011); this is the engineering
side, and the two run in parallel.

> If you are a hiring manager: everything under "Manager prerequisites" must be done
> before the joiner's first day. A joiner who spends week one waiting for access is a
> joiner you lose in month five.

## Manager prerequisites (before day 1)

| # | Item | Where | By |
|---|---|---|---|
| 1 | Hardware requisition raised | NexServe | DOJ − 14 |
| 2 | GitLab group membership requested | NexServe → Access | DOJ − 10 |
| 3 | Jira and Confluence project access requested | NexServe → Access | DOJ − 10 |
| 4 | Buddy nominated and briefed | PeopleHub | DOJ − 10 |
| 5 | Client access request raised with justification | Delivery Manager | DOJ − 7 |
| 6 | First task identified — real, small, reversible | Backlog | DOJ − 5 |
| 7 | 30-60-90 plan drafted | PeopleHub | DOJ − 5 |
| 8 | Team told who is joining, when, and on what | Team channel | DOJ − 3 |

## Day 1 — accounts and machine

Do these in order. Later steps depend on earlier ones.

1. Sign in to Microsoft 365, change the password, enrol MFA in Microsoft Authenticator.
2. Confirm the device shows **Compliant** in NexServe → My Assets. Disk encryption,
   endpoint protection and the DLP agent are pre-installed. A non-compliant device is
   blocked from every client environment, so fix this on day 1, not day 4.
3. Connect to Nexora Secure Access (VPN).
4. Set your Slack display name to your full name. Join `#eng-general`, your site channel
   and your team channel.
5. Log in to GitLab with SSO. Add an SSH key. Confirm you can see the team's group.
6. Log in to Jira. Find the current sprint board. Find the backlog.

## Day 2 — local environment

```
git clone git@gitlab.nexoratech.in:<practice>/<repo>.git
cd <repo>
make bootstrap        # installs toolchain,  hooks and local dependencies
make test             # must be green before you change anything
make run              # starts the service against local stubs
```

If `make test` is not green on a clean clone, that is a bug in the repository, not in
 your setup. Raise it in the team channel — you will not be the only person it has
happened to, and fixing it is a legitimate first contribution.

 Common first-day environment issues:

| Symptom | Cause | Fix |
|---|---|---|
| `make bootstrap` fails on package fetch | Artifactory proxy not on the VPN route | Reconnect the VPN; check the proxy entry in `~/.npmrc` or `settings.xml` |
| SSH to GitLab refused | Key added to the wrong account | Re-add under GitLab → Preferences → SSH Keys with the SSO identity |
| Tests fail on timezone assertions | Local machine not on IST | `sudo systemsetup -settimezone Asia/Kolkata` |
| Docker containers exit immediately | Insufficient memory allocation | Raise Docker Desktop memory to 8 GB |
| Client VPN and Nexora VPN conflict | Two tunnels claiming the default route | Use the split-tunnel profile documented in the engagement runbook |

## Week 1 — how we work

### Branching

`main` is always releasable. Work happens on `feature/<ticket-id>-<short-slug>`.
Rebase before you open a merge request; do not merge `main` into your branch. Squash on
merge so that `main` carries one commit per ticket.

### Merge requests

- Small. A merge request over 400 changed lines will get a slow, shallow review, and
  that is a worse outcome for you than splitting it.
- Description says **what changed and why**, links the ticket, and lists what you

  tested.  "Bug fix" is not a description.
- Two approvals for anything touching a client-facing API, authentication, money
  movement or personal data. One approval otherwise.
- CI green before review is requested.  Do not ask a colleague to babysit a red pipeline.

### Code review

 We review the change, not the person. Reviewers are expected to be specific and to
distinguish clearly between **blocking** ("this will break in production because…") and
**non-blocking** ("consider…"). Authors are expected to respond to every comment, even
if the response is "not doing this, here is why".

The reviewer is accountable for what they approve. That includes AI-assisted code:
review it,  test it, licence-scan it, and treat it as if you had written it yourself.

 ### Definition of done

A story is done when:  the code is merged to `main`; unit and integration tests cover the
new behaviour; the pipeline is green; documentation or the runbook is updated where
behaviour changed; observability exists for anything new that can fail; and the ticket

carries evidence a reviewer could check without asking you.

## Week 2 — client environment

Client access is never automatic. It needs the client's own approval, a named business
justification, a signed client NDA, and in regulated sectors a client-specific training
module. Expect five to fifteen working days.

Before you touch a client environment:

- Read the engagement's Delivery Operating Model. It records the working hours, the
  shift pattern, the escalation path, the data-handling constraints, and whether
  AI-assisted development is permitted for that client. These vary a lot between
  clients.
- Never copy production data into a development or test environment. Use the masked
  extract or the synthetic generator. This is not negotiable and it is audited.
- Never test a change against production personal data, however small the change.
- Report any suspected personal data breach to security-incident@nexoratech.in within
  **one hour**. That timeline is contractual with several clients.

## On-call

You do not join the on-call roster in your first 60 days. When you do:

 1. Shadow two full rotations first.
2. Read the runbook for every service you will be paged for. If a runbook does not
   exist, writing it is part of joining the roster.
3. Confirm your phone receives alerts overnight — test it, do not assume it.
4. On-call allowance is INR 700 per weekday and INR 1,200 per weekend or holiday day of
   roster, plus INR 1,500 per callout resolved outside working hours, capped at two
   callouts per day. Claimed automatically from the roster; check it appears in the
   following month's payslip.

## Escalation

| Problem | First | Then |
|---|---|---|
| Blocked on access after 2 days | NexServe P2 + your manager | IT Support Lead for the site |

| Blocked on client access after 10 days | Delivery Manager | Practice Head |
| Repository broken on a clean clone | Team channel | Tech Lead |
| Something in the codebase you think is unsafe | Tech Lead | Practice Architect |
| You are drowning | Your manager, plainly | Skip-level, or your HRBP |

The last row is real. Saying "I am underwater" in week three is a normal, expected thing
to do and there is no cost to it. The cost lands when it is said in month four.


<!-- Nexora Technologies Private Limited — Confidential — Internal Use Only — exported from the HR content repository -->
<!-- Nexora Technologies Private Limited — Confidential — Internal Use Only -->
