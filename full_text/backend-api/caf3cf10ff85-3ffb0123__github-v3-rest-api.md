---
name: github-v3-rest-api
description: "GitHub v3 REST API skill. Use when working with GitHub v3 REST for root, admin, app. Covers 725 endpoints."
version: 1.0.0
generator: lapsh
---

# GitHub v3 REST API
API version: 1.1.4

## Auth
Requires API key (secret parameter)

## Base URL
{protocol}://{hostname}/api/v3

## Setup
1. Include your API key via the secret parameter
2. GET / -- verify access
3. POST /admin/hooks -- create first hooks

## Endpoints

725 endpoints across 36 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | GitHub API Root |

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/hooks | List global webhooks |
| POST | /admin/hooks | Create a global webhook |
| GET | /admin/hooks/{hook_id} | Get a global webhook |
| PATCH | /admin/hooks/{hook_id} | Update a global webhook |
| DELETE | /admin/hooks/{hook_id} | Delete a global webhook |
| POST | /admin/hooks/{hook_id}/pings | Ping a global webhook |
| GET | /admin/keys | List public keys |
| DELETE | /admin/keys/{key_ids} | Delete a public key |
| PATCH | /admin/ldap/teams/{team_id}/mapping | Update LDAP mapping for a team |
| POST | /admin/ldap/teams/{team_id}/sync | Sync LDAP mapping for a team |
| PATCH | /admin/ldap/users/{username}/mapping | Update LDAP mapping for a user |
| POST | /admin/ldap/users/{username}/sync | Sync LDAP mapping for a user |
| POST | /admin/organizations | Create an organization |
| PATCH | /admin/organizations/{org} | Update an organization name |
| GET | /admin/pre-receive-environments | List pre-receive environments |
| POST | /admin/pre-receive-environments | Create a pre-receive environment |
| GET | /admin/pre-receive-environments/{pre_receive_environment_id} | Get a pre-receive environment |
| PATCH | /admin/pre-receive-environments/{pre_receive_environment_id} | Update a pre-receive environment |
| DELETE | /admin/pre-receive-environments/{pre_receive_environment_id} | Delete a pre-receive environment |
| POST | /admin/pre-receive-environments/{pre_receive_environment_id}/downloads | Start a pre-receive environment download |
| GET | /admin/pre-receive-environments/{pre_receive_environment_id}/downloads/latest | Get the download status for a pre-receive environment |
| GET | /admin/pre-receive-hooks | List pre-receive hooks |
| POST | /admin/pre-receive-hooks | Create a pre-receive hook |
| GET | /admin/pre-receive-hooks/{pre_receive_hook_id} | Get a pre-receive hook |
| PATCH | /admin/pre-receive-hooks/{pre_receive_hook_id} | Update a pre-receive hook |
| DELETE | /admin/pre-receive-hooks/{pre_receive_hook_id} | Delete a pre-receive hook |
| GET | /admin/tokens | List personal access tokens |
| DELETE | /admin/tokens/{token_id} | Delete a personal access token |
| POST | /admin/users | Create a user |
| PATCH | /admin/users/{username} | Update the username for a user |
| DELETE | /admin/users/{username} | Delete a user |
| POST | /admin/users/{username}/authorizations | Create an impersonation OAuth token |
| DELETE | /admin/users/{username}/authorizations | Delete an impersonation OAuth token |

### app
| Method | Path | Description |
|--------|------|-------------|
| GET | /app | Get the authenticated app |
| GET | /app/hook/config | Get a webhook configuration for an app |
| PATCH | /app/hook/config | Update a webhook configuration for an app |
| GET | /app/hook/deliveries | List deliveries for an app webhook |
| GET | /app/hook/deliveries/{delivery_id} | Get a delivery for an app webhook |
| POST | /app/hook/deliveries/{delivery_id}/attempts | Redeliver a delivery for an app webhook |
| GET | /app/installations | List installations for the authenticated app |
| GET | /app/installations/{installation_id} | Get an installation for the authenticated app |
| DELETE | /app/installations/{installation_id} | Delete an installation for the authenticated app |
| POST | /app/installations/{installation_id}/access_tokens | Create an installation access token for an app |
| PUT | /app/installations/{installation_id}/suspended | Suspend an app installation |
| DELETE | /app/installations/{installation_id}/suspended | Unsuspend an app installation |

### app-manifests
| Method | Path | Description |
|--------|------|-------------|
| POST | /app-manifests/{code}/conversions | Create a GitHub App from a manifest |

### applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /applications/grants | List your grants |
| GET | /applications/grants/{grant_id} | Get a single grant |
| DELETE | /applications/grants/{grant_id} | Delete a grant |
| DELETE | /applications/{client_id}/grant | Delete an app authorization |
| DELETE | /applications/{client_id}/grants/{access_token} | Revoke a grant for an application |
| POST | /applications/{client_id}/token | Check a token |
| PATCH | /applications/{client_id}/token | Reset a token |
| DELETE | /applications/{client_id}/token | Delete an app token |
| POST | /applications/{client_id}/token/scoped | Create a scoped access token |
| GET | /applications/{client_id}/tokens/{access_token} | Check an authorization |
| POST | /applications/{client_id}/tokens/{access_token} | Reset an authorization |
| DELETE | /applications/{client_id}/tokens/{access_token} | Revoke an authorization for an application |

### apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps/{app_slug} | Get an app |

### authorizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /authorizations | List your authorizations |
| POST | /authorizations | Create a new authorization |
| PUT | /authorizations/clients/{client_id} | Get-or-create an authorization for a specific app |
| PUT | /authorizations/clients/{client_id}/{fingerprint} | Get-or-create an authorization for a specific app and fingerprint |
| GET | /authorizations/{authorization_id} | Get a single authorization |
| PATCH | /authorizations/{authorization_id} | Update an existing authorization |
| DELETE | /authorizations/{authorization_id} | Delete an authorization |

### codes_of_conduct
| Method | Path | Description |
|--------|------|-------------|
| GET | /codes_of_conduct | Get all codes of conduct |
| GET | /codes_of_conduct/{key} | Get a code of conduct |

### emojis
| Method | Path | Description |
|--------|------|-------------|
| GET | /emojis | Get emojis |

### enterprise
| Method | Path | Description |
|--------|------|-------------|
| GET | /enterprise/announcement | Get the global announcement banner |
| PATCH | /enterprise/announcement | Set the global announcement banner |
| DELETE | /enterprise/announcement | Remove the global announcement banner |
| GET | /enterprise/settings/license | Get license information |
| GET | /enterprise/stats/all | Get all statistics |
| GET | /enterprise/stats/comments | Get comment statistics |
| GET | /enterprise/stats/gists | Get gist statistics |
| GET | /enterprise/stats/hooks | Get hooks statistics |
| GET | /enterprise/stats/issues | Get issue statistics |
| GET | /enterprise/stats/milestones | Get milestone statistics |
| GET | /enterprise/stats/orgs | Get organization statistics |
| GET | /enterprise/stats/pages | Get pages statistics |
| GET | /enterprise/stats/pulls | Get pull request statistics |
| GET | /enterprise/stats/repos | Get repository statistics |
| GET | /enterprise/stats/users | Get users statistics |

### enterprises
| Method | Path | Description |
|--------|------|-------------|
| GET | /enterprises/{enterprise}/actions/permissions | Get GitHub Actions permissions for an enterprise |
| PUT | /enterprises/{enterprise}/actions/permissions | Set GitHub Actions permissions for an enterprise |
| GET | /enterprises/{enterprise}/actions/permissions/organizations | List selected organizations enabled for GitHub Actions in an enterprise |
| PUT | /enterprises/{enterprise}/actions/permissions/organizations | Set selected organizations enabled for GitHub Actions in an enterprise |
| PUT | /enterprises/{enterprise}/actions/permissions/organizations/{org_id} | Enable a selected organization for GitHub Actions in an enterprise |
| DELETE | /enterprises/{enterprise}/actions/permissions/organizations/{org_id} | Disable a selected organization for GitHub Actions in an enterprise |
| GET | /enterprises/{enterprise}/actions/permissions/selected-actions | Get allowed actions for an enterprise |
| PUT | /enterprises/{enterprise}/actions/permissions/selected-actions | Set allowed actions for an enterprise |
| GET | /enterprises/{enterprise}/actions/runner-groups | List self-hosted runner groups for an enterprise |
| POST | /enterprises/{enterprise}/actions/runner-groups | Create a self-hosted runner group for an enterprise |
| GET | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id} | Get a self-hosted runner group for an enterprise |
| PATCH | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id} | Update a self-hosted runner group for an enterprise |
| DELETE | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id} | Delete a self-hosted runner group from an enterprise |
| GET | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations | List organization access to a self-hosted runner group in an enterprise |
| PUT | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations | Set organization access for a self-hosted runner group in an enterprise |
| PUT | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations/{org_id} | Add organization access to a self-hosted runner group in an enterprise |
| DELETE | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations/{org_id} | Remove organization access to a self-hosted runner group in an enterprise |
| GET | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners | List self-hosted runners in a group for an enterprise |
| PUT | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners | Set self-hosted runners in a group for an enterprise |
| PUT | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Add a self-hosted runner to a group for an enterprise |
| DELETE | /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Remove a self-hosted runner from a group for an enterprise |
| GET | /enterprises/{enterprise}/actions/runners | List self-hosted runners for an enterprise |
| GET | /enterprises/{enterprise}/actions/runners/downloads | List runner applications for an enterprise |
| POST | /enterprises/{enterprise}/actions/runners/registration-token | Create a registration token for an enterprise |
| POST | /enterprises/{enterprise}/actions/runners/remove-token | Create a remove token for an enterprise |
| GET | /enterprises/{enterprise}/actions/runners/{runner_id} | Get a self-hosted runner for an enterprise |
| DELETE | /enterprises/{enterprise}/actions/runners/{runner_id} | Delete a self-hosted runner from an enterprise |
| GET | /enterprises/{enterprise}/audit-log | Get the audit log for an enterprise |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | List public events |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| GET | /feeds | Get feeds |

### gists
| Method | Path | Description |
|--------|------|-------------|
| GET | /gists | List gists for the authenticated user |
| POST | /gists | Create a gist |
| GET | /gists/public | List public gists |
| GET | /gists/starred | List starred gists |
| GET | /gists/{gist_id} | Get a gist |
| PATCH | /gists/{gist_id} | Update a gist |
| DELETE | /gists/{gist_id} | Delete a gist |
| GET | /gists/{gist_id}/comments | List gist comments |
| POST | /gists/{gist_id}/comments | Create a gist comment |
| GET | /gists/{gist_id}/comments/{comment_id} | Get a gist comment |
| PATCH | /gists/{gist_id}/comments/{comment_id} | Update a gist comment |
| DELETE | /gists/{gist_id}/comments/{comment_id} | Delete a gist comment |
| GET | /gists/{gist_id}/commits | List gist commits |
| GET | /gists/{gist_id}/forks | List gist forks |
| POST | /gists/{gist_id}/forks | Fork a gist |
| GET | /gists/{gist_id}/star | Check if a gist is starred |
| PUT | /gists/{gist_id}/star | Star a gist |
| DELETE | /gists/{gist_id}/star | Unstar a gist |
| GET | /gists/{gist_id}/{sha} | Get a gist revision |

### gitignore
| Method | Path | Description |
|--------|------|-------------|
| GET | /gitignore/templates | Get all gitignore templates |
| GET | /gitignore/templates/{name} | Get a gitignore template |

### installation
| Method | Path | Description |
|--------|------|-------------|
| GET | /installation/repositories | List repositories accessible to the app installation |
| DELETE | /installation/token | Revoke an installation access token |

### issues
| Method | Path | Description |
|--------|------|-------------|
| GET | /issues | List issues assigned to the authenticated user |

### licenses
| Method | Path | Description |
|--------|------|-------------|
| GET | /licenses | Get all commonly used licenses |
| GET | /licenses/{license} | Get a license |

### markdown
| Method | Path | Description |
|--------|------|-------------|
| POST | /markdown | Render a Markdown document |
| POST | /markdown/raw | Render a Markdown document in raw mode |

### meta
| Method | Path | Description |
|--------|------|-------------|
| GET | /meta | Get GitHub Enterprise Server meta information |

### networks
| Method | Path | Description |
|--------|------|-------------|
| GET | /networks/{owner}/{repo}/events | List public events for a network of repositories |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications | List notifications for the authenticated user |
| PUT | /notifications | Mark notifications as read |
| GET | /notifications/threads/{thread_id} | Get a thread |
| PATCH | /notifications/threads/{thread_id} | Mark a thread as read |
| GET | /notifications/threads/{thread_id}/subscription | Get a thread subscription for the authenticated user |
| PUT | /notifications/threads/{thread_id}/subscription | Set a thread subscription |
| DELETE | /notifications/threads/{thread_id}/subscription | Delete a thread subscription |

### octocat
| Method | Path | Description |
|--------|------|-------------|
| GET | /octocat | Get Octocat |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations | List organizations |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| GET | /orgs/{org} | Get an organization |
| PATCH | /orgs/{org} | Update an organization |
| GET | /orgs/{org}/actions/permissions | Get GitHub Actions permissions for an organization |
| PUT | /orgs/{org}/actions/permissions | Set GitHub Actions permissions for an organization |
| GET | /orgs/{org}/actions/permissions/repositories | List selected repositories enabled for GitHub Actions in an organization |
| PUT | /orgs/{org}/actions/permissions/repositories | Set selected repositories enabled for GitHub Actions in an organization |
| PUT | /orgs/{org}/actions/permissions/repositories/{repository_id} | Enable a selected repository for GitHub Actions in an organization |
| DELETE | /orgs/{org}/actions/permissions/repositories/{repository_id} | Disable a selected repository for GitHub Actions in an organization |
| GET | /orgs/{org}/actions/permissions/selected-actions | Get allowed actions for an organization |
| PUT | /orgs/{org}/actions/permissions/selected-actions | Set allowed actions for an organization |
| GET | /orgs/{org}/actions/runner-groups | List self-hosted runner groups for an organization |
| POST | /orgs/{org}/actions/runner-groups | Create a self-hosted runner group for an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id} | Get a self-hosted runner group for an organization |
| PATCH | /orgs/{org}/actions/runner-groups/{runner_group_id} | Update a self-hosted runner group for an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id} | Delete a self-hosted runner group from an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories | List repository access to a self-hosted runner group in an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories | Set repository access for a self-hosted runner group in an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id} | Add repository access to a self-hosted runner group in an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id} | Remove repository access to a self-hosted runner group in an organization |
| GET | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners | List self-hosted runners in a group for an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners | Set self-hosted runners in a group for an organization |
| PUT | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Add a self-hosted runner to a group for an organization |
| DELETE | /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id} | Remove a self-hosted runner from a group for an organization |
| GET | /orgs/{org}/actions/runners | List self-hosted runners for an organization |
| GET | /orgs/{org}/actions/runners/downloads | List runner applications for an organization |
| POST | /orgs/{org}/actions/runners/registration-token | Create a registration token for an organization |
| POST | /orgs/{org}/actions/runners/remove-token | Create a remove token for an organization |
| GET | /orgs/{org}/actions/runners/{runner_id} | Get a self-hosted runner for an organization |
| DELETE | /orgs/{org}/actions/runners/{runner_id} | Delete a self-hosted runner from an organization |
| GET | /orgs/{org}/actions/secrets | List organization secrets |
| GET | /orgs/{org}/actions/secrets/public-key | Get an organization public key |
| GET | /orgs/{org}/actions/secrets/{secret_name} | Get an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name} | Create or update an organization secret |
| DELETE | /orgs/{org}/actions/secrets/{secret_name} | Delete an organization secret |
| GET | /orgs/{org}/actions/secrets/{secret_name}/repositories | List selected repositories for an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name}/repositories | Set selected repositories for an organization secret |
| PUT | /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id} | Add selected repository to an organization secret |
| DELETE | /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id} | Remove selected repository from an organization secret |
| GET | /orgs/{org}/audit-log | Get the audit log for an organization |
| GET | /orgs/{org}/events | List public organization events |
| GET | /orgs/{org}/hooks | List organization webhooks |
| POST | /orgs/{org}/hooks | Create an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id} | Get an organization webhook |
| PATCH | /orgs/{org}/hooks/{hook_id} | Update an organization webhook |
| DELETE | /orgs/{org}/hooks/{hook_id} | Delete an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id}/config | Get a webhook configuration for an organization |
| PATCH | /orgs/{org}/hooks/{hook_id}/config | Update a webhook configuration for an organization |
| GET | /orgs/{org}/hooks/{hook_id}/deliveries | List deliveries for an organization webhook |
| GET | /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id} | Get a webhook delivery for an organization webhook |
| POST | /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}/attempts | Redeliver a delivery for an organization webhook |
| POST | /orgs/{org}/hooks/{hook_id}/pings | Ping an organization webhook |
| GET | /orgs/{org}/installation | Get an organization installation for the authenticated app |
| GET | /orgs/{org}/installations | List app installations for an organization |
| GET | /orgs/{org}/issues | List organization issues assigned to the authenticated user |
| GET | /orgs/{org}/members | List organization members |
| GET | /orgs/{org}/members/{username} | Check organization membership for a user |
| DELETE | /orgs/{org}/members/{username} | Remove an organization member |
| GET | /orgs/{org}/memberships/{username} | Get organization membership for a user |
| PUT | /orgs/{org}/memberships/{username} | Set organization membership for a user |
| DELETE | /orgs/{org}/memberships/{username} | Remove organization membership for a user |
| GET | /orgs/{org}/outside_collaborators | List outside collaborators for an organization |
| PUT | /orgs/{org}/outside_collaborators/{username} | Convert an organization member to outside collaborator |
| DELETE | /orgs/{org}/outside_collaborators/{username} | Remove outside collaborator from an organization |
| GET | /orgs/{org}/pre-receive-hooks | List pre-receive hooks for an organization |
| GET | /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id} | Get a pre-receive hook for an organization |
| PATCH | /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id} | Update pre-receive hook enforcement for an organization |
| DELETE | /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id} | Remove pre-receive hook enforcement for an organization |
| GET | /orgs/{org}/projects | List organization projects |
| POST | /orgs/{org}/projects | Create an organization project |
| GET | /orgs/{org}/public_members | List public organization members |
| GET | /orgs/{org}/public_members/{username} | Check public organization membership for a user |
| PUT | /orgs/{org}/public_members/{username} | Set public organization membership for the authenticated user |
| DELETE | /orgs/{org}/public_members/{username} | Remove public organization membership for the authenticated user |
| GET | /orgs/{org}/repos | List organization repositories |
| POST | /orgs/{org}/repos | Create an organization repository |
| GET | /orgs/{org}/secret-scanning/alerts | List secret scanning alerts for an organization |
| GET | /orgs/{org}/teams | List teams |
| POST | /orgs/{org}/teams | Create a team |
| GET | /orgs/{org}/teams/{team_slug} | Get a team by name |
| PATCH | /orgs/{org}/teams/{team_slug} | Update a team |
| DELETE | /orgs/{org}/teams/{team_slug} | Delete a team |
| GET | /orgs/{org}/teams/{team_slug}/discussions | List discussions |
| POST | /orgs/{org}/teams/{team_slug}/discussions | Create a discussion |
| GET | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number} | Get a discussion |
| PATCH | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number} | Update a discussion |
| DELETE | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number} | Delete a discussion |
| GET | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments | List discussion comments |
| POST | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments | Create a discussion comment |
| GET | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number} | Get a discussion comment |
| PATCH | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number} | Update a discussion comment |
| DELETE | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number} | Delete a discussion comment |
| GET | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions | List reactions for a team discussion comment |
| POST | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions | Create reaction for a team discussion comment |
| DELETE | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions/{reaction_id} | Delete team discussion comment reaction |
| GET | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions | List reactions for a team discussion |
| POST | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions | Create reaction for a team discussion |
| DELETE | /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions/{reaction_id} | Delete team discussion reaction |
| GET | /orgs/{org}/teams/{team_slug}/members | List team members |
| GET | /orgs/{org}/teams/{team_slug}/memberships/{username} | Get team membership for a user |
| PUT | /orgs/{org}/teams/{team_slug}/memberships/{username} | Add or update team membership for a user |
| DELETE | /orgs/{org}/teams/{team_slug}/memberships/{username} | Remove team membership for a user |
| GET | /orgs/{org}/teams/{team_slug}/projects | List team projects |
| GET | /orgs/{org}/teams/{team_slug}/projects/{project_id} | Check team permissions for a project |
| PUT | /orgs/{org}/teams/{team_slug}/projects/{project_id} | Add or update team project permissions |
| DELETE | /orgs/{org}/teams/{team_slug}/projects/{project_id} | Remove a project from a team |
| GET | /orgs/{org}/teams/{team_slug}/repos | List team repositories |
| GET | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Check team permissions for a repository |
| PUT | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Add or update team repository permissions |
| DELETE | /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} | Remove a repository from a team |
| GET | /orgs/{org}/teams/{team_slug}/teams | List child teams |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/columns/cards/{card_id} | Get a project card |
| PATCH | /projects/columns/cards/{card_id} | Update an existing project card |
| DELETE | /projects/columns/cards/{card_id} | Delete a project card |
| POST | /projects/columns/cards/{card_id}/moves | Move a project card |
| GET | /projects/columns/{column_id} | Get a project column |
| PATCH | /projects/columns/{column_id} | Update an existing project column |
| DELETE | /projects/columns/{column_id} | Delete a project column |
| GET | /projects/columns/{column_id}/cards | List project cards |
| POST | /projects/columns/{column_id}/cards | Create a project card |
| POST | /projects/columns/{column_id}/moves | Move a project column |
| GET | /projects/{project_id} | Get a project |
| PATCH | /projects/{project_id} | Update a project |
| DELETE | /projects/{project_id} | Delete a project |
| GET | /projects/{project_id}/collaborators | List project collaborators |
| PUT | /projects/{project_id}/collaborators/{username} | Add project collaborator |
| DELETE | /projects/{project_id}/collaborators/{username} | Remove user as a collaborator |
| GET | /projects/{project_id}/collaborators/{username}/permission | Get project permission for a user |
| GET | /projects/{project_id}/columns | List project columns |
| POST | /projects/{project_id}/columns | Create a project column |

### rate_limit
| Method | Path | Description |
|--------|------|-------------|
| GET | /rate_limit | Get rate limit status for the authenticated user |

### reactions
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /reactions/{reaction_id} | Delete a reaction (Legacy) |

### repos
| Method | Path | Description |
|--------|------|-------------|
| GET | /repos/{owner}/{repo} | Get a repository |
| PATCH | /repos/{owner}/{repo} | Update a repository |
| DELETE | /repos/{owner}/{repo} | Delete a repository |
| GET | /repos/{owner}/{repo}/actions/artifacts | List artifacts for a repository |
| GET | /repos/{owner}/{repo}/actions/artifacts/{artifact_id} | Get an artifact |
| DELETE | /repos/{owner}/{repo}/actions/artifacts/{artifact_id} | Delete an artifact |
| GET | /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format} | Download an artifact |
| GET | /repos/{owner}/{repo}/actions/jobs/{job_id} | Get a job for a workflow run |
| GET | /repos/{owner}/{repo}/actions/jobs/{job_id}/logs | Download job logs for a workflow run |
| GET | /repos/{owner}/{repo}/actions/permissions | Get GitHub Actions permissions for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions | Set GitHub Actions permissions for a repository |
| GET | /repos/{owner}/{repo}/actions/permissions/selected-actions | Get allowed actions for a repository |
| PUT | /repos/{owner}/{repo}/actions/permissions/selected-actions | Set allowed actions for a repository |
| GET | /repos/{owner}/{repo}/actions/runners | List self-hosted runners for a repository |
| GET | /repos/{owner}/{repo}/actions/runners/downloads | List runner applications for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/registration-token | Create a registration token for a repository |
| POST | /repos/{owner}/{repo}/actions/runners/remove-token | Create a remove token for a repository |
| GET | /repos/{owner}/{repo}/actions/runners/{runner_id} | Get a self-hosted runner for a repository |
| DELETE | /repos/{owner}/{repo}/actions/runners/{runner_id} | Delete a self-hosted runner from a repository |
| GET | /repos/{owner}/{repo}/actions/runs | List workflow runs for a repository |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id} | Get a workflow run |
| DELETE | /repos/{owner}/{repo}/actions/runs/{run_id} | Delete a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/approvals | Get the review history for a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts | List workflow run artifacts |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/cancel | Cancel a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/jobs | List jobs for a workflow run |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/logs | Download workflow run logs |
| DELETE | /repos/{owner}/{repo}/actions/runs/{run_id}/logs | Delete workflow run logs |
| GET | /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments | Get pending deployments for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments | Review pending deployments for a workflow run |
| POST | /repos/{owner}/{repo}/actions/runs/{run_id}/rerun | Re-run a workflow |
| GET | /repos/{owner}/{repo}/actions/secrets | List repository secrets |
| GET | /repos/{owner}/{repo}/actions/secrets/public-key | Get a repository public key |
| GET | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Get a repository secret |
| PUT | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Create or update a repository secret |
| DELETE | /repos/{owner}/{repo}/actions/secrets/{secret_name} | Delete a repository secret |
| GET | /repos/{owner}/{repo}/actions/workflows | List repository workflows |
| GET | /repos/{owner}/{repo}/actions/workflows/{workflow_id} | Get a workflow |
| PUT | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/disable | Disable a workflow |
| POST | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches | Create a workflow dispatch event |
| PUT | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/enable | Enable a workflow |
| GET | /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs | List workflow runs for a workflow |
| GET | /repos/{owner}/{repo}/assignees | List assignees |
| GET | /repos/{owner}/{repo}/assignees/{assignee} | Check if a user can be assigned |
| GET | /repos/{owner}/{repo}/autolinks | List all autolinks of a repository |
| POST | /repos/{owner}/{repo}/autolinks | Create an autolink reference for a repository |
| GET | /repos/{owner}/{repo}/autolinks/{autolink_id} | Get an autolink reference of a repository |
| DELETE | /repos/{owner}/{repo}/autolinks/{autolink_id} | Delete an autolink reference from a repository |
| GET | /repos/{owner}/{repo}/branches | List branches |
| GET | /repos/{owner}/{repo}/branches/{branch} | Get a branch |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection | Get branch protection |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection | Update branch protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection | Delete branch protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Get admin branch protection |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Set admin branch protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins | Delete admin branch protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Get pull request review protection |
| PATCH | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Update pull request review protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews | Delete pull request review protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Get commit signature protection |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Create commit signature protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures | Delete commit signature protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Get status checks protection |
| PATCH | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Update status check protection |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks | Remove status check protection |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Get all status check contexts |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Add status check contexts |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Set status check contexts |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts | Remove status check contexts |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions | Get access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions | Delete access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Get apps with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Add app access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Set app access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps | Remove app access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Get teams with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Add team access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Set team access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams | Remove team access restrictions |
| GET | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Get users with access to the protected branch |
| POST | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Add user access restrictions |
| PUT | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Set user access restrictions |
| DELETE | /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users | Remove user access restrictions |
| POST | /repos/{owner}/{repo}/branches/{branch}/rename | Rename a branch |
| POST | /repos/{owner}/{repo}/check-runs | Create a check run |
| GET | /repos/{owner}/{repo}/check-runs/{check_run_id} | Get a check run |
| PATCH | /repos/{owner}/{repo}/check-runs/{check_run_id} | Update a check run |
| GET | /repos/{owner}/{repo}/check-runs/{check_run_id}/annotations | List check run annotations |
| POST | /repos/{owner}/{repo}/check-runs/{check_run_id}/rerequest | Rerequest a check run |
| POST | /repos/{owner}/{repo}/check-suites | Create a check suite |
| PATCH | /repos/{owner}/{repo}/check-suites/preferences | Update repository preferences for check suites |
| GET | /repos/{owner}/{repo}/check-suites/{check_suite_id} | Get a check suite |
| GET | /repos/{owner}/{repo}/check-suites/{check_suite_id}/check-runs | List check runs in a check suite |
| POST | /repos/{owner}/{repo}/check-suites/{check_suite_id}/rerequest | Rerequest a check suite |
| GET | /repos/{owner}/{repo}/code-scanning/alerts | List code scanning alerts for a repository |
| GET | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number} | Get a code scanning alert |
| PATCH | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number} | Update a code scanning alert |
| GET | /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/instances | List instances of a code scanning alert |
| GET | /repos/{owner}/{repo}/code-scanning/analyses | List code scanning analyses for a repository |
| GET | /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id} | Get a code scanning analysis for a repository |
| DELETE | /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id} | Delete a code scanning analysis from a repository |
| POST | /repos/{owner}/{repo}/code-scanning/sarifs | Upload an analysis as SARIF data |
| GET | /repos/{owner}/{repo}/code-scanning/sarifs/{sarif_id} | Get information about a SARIF upload |
| GET | /repos/{owner}/{repo}/collaborators | List repository collaborators |
| GET | /repos/{owner}/{repo}/collaborators/{username} | Check if a user is a repository collaborator |
| PUT | /repos/{owner}/{repo}/collaborators/{username} | Add a repository collaborator |
| DELETE | /repos/{owner}/{repo}/collaborators/{username} | Remove a repository collaborator |
| GET | /repos/{owner}/{repo}/collaborators/{username}/permission | Get repository permissions for a user |
| GET | /repos/{owner}/{repo}/comments | List commit comments for a repository |
| GET | /repos/{owner}/{repo}/comments/{comment_id} | Get a commit comment |
| PATCH | /repos/{owner}/{repo}/comments/{comment_id} | Update a commit comment |
| DELETE | /repos/{owner}/{repo}/comments/{comment_id} | Delete a commit comment |
| GET | /repos/{owner}/{repo}/comments/{comment_id}/reactions | List reactions for a commit comment |
| POST | /repos/{owner}/{repo}/comments/{comment_id}/reactions | Create reaction for a commit comment |
| DELETE | /repos/{owner}/{repo}/comments/{comment_id}/reactions/{reaction_id} | Delete a commit comment reaction |
| GET | /repos/{owner}/{repo}/commits | List commits |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/branches-where-head | List branches for HEAD commit |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/comments | List commit comments |
| POST | /repos/{owner}/{repo}/commits/{commit_sha}/comments | Create a commit comment |
| GET | /repos/{owner}/{repo}/commits/{commit_sha}/pulls | List pull requests associated with a commit |
| GET | /repos/{owner}/{repo}/commits/{ref} | Get a commit |
| GET | /repos/{owner}/{repo}/commits/{ref}/check-runs | List check runs for a Git reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/check-suites | List check suites for a Git reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/status | Get the combined status for a specific reference |
| GET | /repos/{owner}/{repo}/commits/{ref}/statuses | List commit statuses for a reference |
| GET | /repos/{owner}/{repo}/compare/{basehead} | Compare two commits |
| POST | /repos/{owner}/{repo}/content_references/{content_reference_id}/attachments | Create a content attachment |
| GET | /repos/{owner}/{repo}/contents/{path} | Get repository content |
| PUT | /repos/{owner}/{repo}/contents/{path} | Create or update file contents |
| DELETE | /repos/{owner}/{repo}/contents/{path} | Delete a file |
| GET | /repos/{owner}/{repo}/contributors | List repository contributors |
| GET | /repos/{owner}/{repo}/deployments | List deployments |
| POST | /repos/{owner}/{repo}/deployments | Create a deployment |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id} | Get a deployment |
| DELETE | /repos/{owner}/{repo}/deployments/{deployment_id} | Delete a deployment |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses | List deployment statuses |
| POST | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses | Create a deployment status |
| GET | /repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id} | Get a deployment status |
| POST | /repos/{owner}/{repo}/dispatches | Create a repository dispatch event |
| GET | /repos/{owner}/{repo}/environments | List environments |
| GET | /repos/{owner}/{repo}/environments/{environment_name} | Get an environment |
| PUT | /repos/{owner}/{repo}/environments/{environment_name} | Create or update an environment |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name} | Delete an environment |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies | List deployment branch policies |
| POST | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies | Create a deployment branch policy |
| GET | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Get a deployment branch policy |
| PUT | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Update a deployment branch policy |
| DELETE | /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id} | Delete a deployment branch policy |
| GET | /repos/{owner}/{repo}/events | List repository events |
| GET | /repos/{owner}/{repo}/forks | List forks |
| POST | /repos/{owner}/{repo}/forks | Create a fork |
| POST | /repos/{owner}/{repo}/git/blobs | Create a blob |
| GET | /repos/{owner}/{repo}/git/blobs/{file_sha} | Get a blob |
| POST | /repos/{owner}/{repo}/git/commits | Create a commit |
| GET | /repos/{owner}/{repo}/git/commits/{commit_sha} | Get a commit |
| GET | /repos/{owner}/{repo}/git/matching-refs/{ref} | List matching references |
| GET | /repos/{owner}/{repo}/git/ref/{ref} | Get a reference |
| POST | /repos/{owner}/{repo}/git/refs | Create a reference |
| PATCH | /repos/{owner}/{repo}/git/refs/{ref} | Update a reference |
| DELETE | /repos/{owner}/{repo}/git/refs/{ref} | Delete a reference |
| POST | /repos/{owner}/{repo}/git/tags | Create a tag object |
| GET | /repos/{owner}/{repo}/git/tags/{tag_sha} | Get a tag |
| POST | /repos/{owner}/{repo}/git/trees | Create a tree |
| GET | /repos/{owner}/{repo}/git/trees/{tree_sha} | Get a tree |
| GET | /repos/{owner}/{repo}/hooks | List repository webhooks |
| POST | /repos/{owner}/{repo}/hooks | Create a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id} | Get a repository webhook |
| PATCH | /repos/{owner}/{repo}/hooks/{hook_id} | Update a repository webhook |
| DELETE | /repos/{owner}/{repo}/hooks/{hook_id} | Delete a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/config | Get a webhook configuration for a repository |
| PATCH | /repos/{owner}/{repo}/hooks/{hook_id}/config | Update a webhook configuration for a repository |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries | List deliveries for a repository webhook |
| GET | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id} | Get a delivery for a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts | Redeliver a delivery for a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/pings | Ping a repository webhook |
| POST | /repos/{owner}/{repo}/hooks/{hook_id}/tests | Test the push repository webhook |
| GET | /repos/{owner}/{repo}/installation | Get a repository installation for the authenticated app |
| GET | /repos/{owner}/{repo}/invitations | List repository invitations |
| PATCH | /repos/{owner}/{repo}/invitations/{invitation_id} | Update a repository invitation |
| DELETE | /repos/{owner}/{repo}/invitations/{invitation_id} | Delete a repository invitation |
| GET | /repos/{owner}/{repo}/issues | List repository issues |
| POST | /repos/{owner}/{repo}/issues | Create an issue |
| GET | /repos/{owner}/{repo}/issues/comments | List issue comments for a repository |
| GET | /repos/{owner}/{repo}/issues/comments/{comment_id} | Get an issue comment |
| PATCH | /repos/{owner}/{repo}/issues/comments/{comment_id} | Update an issue comment |
| DELETE | /repos/{owner}/{repo}/issues/comments/{comment_id} | Delete an issue comment |
| GET | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions | List reactions for an issue comment |
| POST | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions | Create reaction for an issue comment |
| DELETE | /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id} | Delete an issue comment reaction |
| GET | /repos/{owner}/{repo}/issues/events | List issue events for a repository |
| GET | /repos/{owner}/{repo}/issues/events/{event_id} | Get an issue event |
| GET | /repos/{owner}/{repo}/issues/{issue_number} | Get an issue |
| PATCH | /repos/{owner}/{repo}/issues/{issue_number} | Update an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/assignees | Add assignees to an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/assignees | Remove assignees from an issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/assignees/{assignee} | Check if a user can be assigned to a issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/comments | List issue comments |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/comments | Create an issue comment |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/events | List issue events |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/labels | List labels for an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/labels | Add labels to an issue |
| PUT | /repos/{owner}/{repo}/issues/{issue_number}/labels | Set labels for an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/labels | Remove all labels from an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/labels/{name} | Remove a label from an issue |
| PUT | /repos/{owner}/{repo}/issues/{issue_number}/lock | Lock an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/lock | Unlock an issue |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/reactions | List reactions for an issue |
| POST | /repos/{owner}/{repo}/issues/{issue_number}/reactions | Create reaction for an issue |
| DELETE | /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id} | Delete an issue reaction |
| GET | /repos/{owner}/{repo}/issues/{issue_number}/timeline | List timeline events for an issue |
| GET | /repos/{owner}/{repo}/keys | List deploy keys |
| POST | /repos/{owner}/{repo}/keys | Create a deploy key |
| GET | /repos/{owner}/{repo}/keys/{key_id} | Get a deploy key |
| DELETE | /repos/{owner}/{repo}/keys/{key_id} | Delete a deploy key |
| GET | /repos/{owner}/{repo}/labels | List labels for a repository |
| POST | /repos/{owner}/{repo}/labels | Create a label |
| GET | /repos/{owner}/{repo}/labels/{name} | Get a label |
| PATCH | /repos/{owner}/{repo}/labels/{name} | Update a label |
| DELETE | /repos/{owner}/{repo}/labels/{name} | Delete a label |
| GET | /repos/{owner}/{repo}/languages | List repository languages |
| PUT | /repos/{owner}/{repo}/lfs | Enable Git LFS for a repository |
| DELETE | /repos/{owner}/{repo}/lfs | Disable Git LFS for a repository |
| GET | /repos/{owner}/{repo}/license | Get the license for a repository |
| POST | /repos/{owner}/{repo}/merge-upstream | Sync a fork branch with the upstream repository |
| POST | /repos/{owner}/{repo}/merges | Merge a branch |
| GET | /repos/{owner}/{repo}/milestones | List milestones |
| POST | /repos/{owner}/{repo}/milestones | Create a milestone |
| GET | /repos/{owner}/{repo}/milestones/{milestone_number} | Get a milestone |
| PATCH | /repos/{owner}/{repo}/milestones/{milestone_number} | Update a milestone |
| DELETE | /repos/{owner}/{repo}/milestones/{milestone_number} | Delete a milestone |
| GET | /repos/{owner}/{repo}/milestones/{milestone_number}/labels | List labels for issues in a milestone |
| GET | /repos/{owner}/{repo}/notifications | List repository notifications for the authenticated user |
| PUT | /repos/{owner}/{repo}/notifications | Mark repository notifications as read |
| GET | /repos/{owner}/{repo}/pages | Get a GitHub Enterprise Server Pages site |
| POST | /repos/{owner}/{repo}/pages | Create a GitHub Enterprise Server Pages site |
| PUT | /repos/{owner}/{repo}/pages | Update information about a GitHub Enterprise Server Pages site |
| DELETE | /repos/{owner}/{repo}/pages | Delete a GitHub Enterprise Server Pages site |
| GET | /repos/{owner}/{repo}/pages/builds | List GitHub Enterprise Server Pages builds |
| POST | /repos/{owner}/{repo}/pages/builds | Request a GitHub Enterprise Server Pages build |
| GET | /repos/{owner}/{repo}/pages/builds/latest | Get latest Pages build |
| GET | /repos/{owner}/{repo}/pages/builds/{build_id} | Get GitHub Enterprise Server Pages build |
| GET | /repos/{owner}/{repo}/pre-receive-hooks | List pre-receive hooks for a repository |
| GET | /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id} | Get a pre-receive hook for a repository |
| PATCH | /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id} | Update pre-receive hook enforcement for a repository |
| DELETE | /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id} | Remove pre-receive hook enforcement for a repository |
| GET | /repos/{owner}/{repo}/projects | List repository projects |
| POST | /repos/{owner}/{repo}/projects | Create a repository project |
| GET | /repos/{owner}/{repo}/pulls | List pull requests |
| POST | /repos/{owner}/{repo}/pulls | Create a pull request |
| GET | /repos/{owner}/{repo}/pulls/comments | List review comments in a repository |
| GET | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Get a review comment for a pull request |
| PATCH | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Update a review comment for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/comments/{comment_id} | Delete a review comment for a pull request |
| GET | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions | List reactions for a pull request review comment |
| POST | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions | Create reaction for a pull request review comment |
| DELETE | /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions/{reaction_id} | Delete a pull request comment reaction |
| GET | /repos/{owner}/{repo}/pulls/{pull_number} | Get a pull request |
| PATCH | /repos/{owner}/{repo}/pulls/{pull_number} | Update a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/comments | List review comments on a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/comments | Create a review comment for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies | Create a reply for a review comment |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/commits | List commits on a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/files | List pull requests files |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/merge | Check if a pull request has been merged |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/merge | Merge a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Get all requested reviewers for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Request reviewers for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers | Remove requested reviewers from a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews | List reviews for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/reviews | Create a review for a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Get a review for a pull request |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Update a review for a pull request |
| DELETE | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} | Delete a pending review for a pull request |
| GET | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments | List comments for a pull request review |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals | Dismiss a review for a pull request |
| POST | /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events | Submit a review for a pull request |
| PUT | /repos/{owner}/{repo}/pulls/{pull_number}/update-branch | Update a pull request branch |
| GET | /repos/{owner}/{repo}/readme | Get a repository README |
| GET | /repos/{owner}/{repo}/readme/{dir} | Get a repository README for a directory |
| GET | /repos/{owner}/{repo}/releases | List releases |
| POST | /repos/{owner}/{repo}/releases | Create a release |
| GET | /repos/{owner}/{repo}/releases/assets/{asset_id} | Get a release asset |
| PATCH | /repos/{owner}/{repo}/releases/assets/{asset_id} | Update a release asset |
| DELETE | /repos/{owner}/{repo}/releases/assets/{asset_id} | Delete a release asset |
| POST | /repos/{owner}/{repo}/releases/generate-notes | Generate release notes content for a release |
| GET | /repos/{owner}/{repo}/releases/latest | Get the latest release |
| GET | /repos/{owner}/{repo}/releases/tags/{tag} | Get a release by tag name |
| GET | /repos/{owner}/{repo}/releases/{release_id} | Get a release |
| PATCH | /repos/{owner}/{repo}/releases/{release_id} | Update a release |
| DELETE | /repos/{owner}/{repo}/releases/{release_id} | Delete a release |
| GET | /repos/{owner}/{repo}/releases/{release_id}/assets | List release assets |
| POST | /repos/{owner}/{repo}/releases/{release_id}/assets | Upload a release asset |
| GET | /repos/{owner}/{repo}/releases/{release_id}/reactions | List reactions for a release |
| POST | /repos/{owner}/{repo}/releases/{release_id}/reactions | Create reaction for a release |
| DELETE | /repos/{owner}/{repo}/releases/{release_id}/reactions/{reaction_id} | Delete a release reaction |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts | List secret scanning alerts for a repository |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} | Get a secret scanning alert |
| PATCH | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} | Update a secret scanning alert |
| GET | /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}/locations | List locations for a secret scanning alert |
| GET | /repos/{owner}/{repo}/stargazers | List stargazers |
| GET | /repos/{owner}/{repo}/stats/code_frequency | Get the weekly commit activity |
| GET | /repos/{owner}/{repo}/stats/commit_activity | Get the last year of commit activity |
| GET | /repos/{owner}/{repo}/stats/contributors | Get all contributor commit activity |
| GET | /repos/{owner}/{repo}/stats/participation | Get the weekly commit count |
| GET | /repos/{owner}/{repo}/stats/punch_card | Get the hourly commit count for each day |
| POST | /repos/{owner}/{repo}/statuses/{sha} | Create a commit status |
| GET | /repos/{owner}/{repo}/subscribers | List watchers |
| GET | /repos/{owner}/{repo}/subscription | Get a repository subscription |
| PUT | /repos/{owner}/{repo}/subscription | Set a repository subscription |
| DELETE | /repos/{owner}/{repo}/subscription | Delete a repository subscription |
| GET | /repos/{owner}/{repo}/tags | List repository tags |
| GET | /repos/{owner}/{repo}/tarball/{ref} | Download a repository archive (tar) |
| GET | /repos/{owner}/{repo}/teams | List repository teams |
| GET | /repos/{owner}/{repo}/topics | Get all repository topics |
| PUT | /repos/{owner}/{repo}/topics | Replace all repository topics |
| POST | /repos/{owner}/{repo}/transfer | Transfer a repository |
| GET | /repos/{owner}/{repo}/zipball/{ref} | Download a repository archive (zip) |
| POST | /repos/{template_owner}/{template_repo}/generate | Create a repository using a template |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| GET | /repositories | List public repositories |
| GET | /repositories/{repository_id}/environments/{environment_name}/secrets | List environment secrets |
| GET | /repositories/{repository_id}/environments/{environment_name}/secrets/public-key | Get an environment public key |
| GET | /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name} | Get an environment secret |
| PUT | /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name} | Create or update an environment secret |
| DELETE | /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name} | Delete an environment secret |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/code | Search code |
| GET | /search/commits | Search commits |
| GET | /search/issues | Search issues and pull requests |
| GET | /search/labels | Search labels |
| GET | /search/repositories | Search repositories |
| GET | /search/topics | Search topics |
| GET | /search/users | Search users |

### setup
| Method | Path | Description |
|--------|------|-------------|
| GET | /setup/api/configcheck | Get the configuration status |
| POST | /setup/api/configure | Start a configuration process |
| GET | /setup/api/maintenance | Get the maintenance status |
| POST | /setup/api/maintenance | Enable or disable maintenance mode |
| GET | /setup/api/settings | Get settings |
| PUT | /setup/api/settings | Set settings |
| GET | /setup/api/settings/authorized-keys | Get all authorized SSH keys |
| POST | /setup/api/settings/authorized-keys | Add an authorized SSH key |
| DELETE | /setup/api/settings/authorized-keys | Remove an authorized SSH key |
| POST | /setup/api/start | Create a GitHub license |
| POST | /setup/api/upgrade | Upgrade a license |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/{team_id} | Get a team (Legacy) |
| PATCH | /teams/{team_id} | Update a team (Legacy) |
| DELETE | /teams/{team_id} | Delete a team (Legacy) |
| GET | /teams/{team_id}/discussions | List discussions (Legacy) |
| POST | /teams/{team_id}/discussions | Create a discussion (Legacy) |
| GET | /teams/{team_id}/discussions/{discussion_number} | Get a discussion (Legacy) |
| PATCH | /teams/{team_id}/discussions/{discussion_number} | Update a discussion (Legacy) |
| DELETE | /teams/{team_id}/discussions/{discussion_number} | Delete a discussion (Legacy) |
| GET | /teams/{team_id}/discussions/{discussion_number}/comments | List discussion comments (Legacy) |
| POST | /teams/{team_id}/discussions/{discussion_number}/comments | Create a discussion comment (Legacy) |
| GET | /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number} | Get a discussion comment (Legacy) |
| PATCH | /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number} | Update a discussion comment (Legacy) |
| DELETE | /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number} | Delete a discussion comment (Legacy) |
| GET | /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions | List reactions for a team discussion comment (Legacy) |
| POST | /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions | Create reaction for a team discussion comment (Legacy) |
| GET | /teams/{team_id}/discussions/{discussion_number}/reactions | List reactions for a team discussion (Legacy) |
| POST | /teams/{team_id}/discussions/{discussion_number}/reactions | Create reaction for a team discussion (Legacy) |
| GET | /teams/{team_id}/members | List team members (Legacy) |
| GET | /teams/{team_id}/members/{username} | Get team member (Legacy) |
| PUT | /teams/{team_id}/members/{username} | Add team member (Legacy) |
| DELETE | /teams/{team_id}/members/{username} | Remove team member (Legacy) |
| GET | /teams/{team_id}/memberships/{username} | Get team membership for a user (Legacy) |
| PUT | /teams/{team_id}/memberships/{username} | Add or update team membership for a user (Legacy) |
| DELETE | /teams/{team_id}/memberships/{username} | Remove team membership for a user (Legacy) |
| GET | /teams/{team_id}/projects | List team projects (Legacy) |
| GET | /teams/{team_id}/projects/{project_id} | Check team permissions for a project (Legacy) |
| PUT | /teams/{team_id}/projects/{project_id} | Add or update team project permissions (Legacy) |
| DELETE | /teams/{team_id}/projects/{project_id} | Remove a project from a team (Legacy) |
| GET | /teams/{team_id}/repos | List team repositories (Legacy) |
| GET | /teams/{team_id}/repos/{owner}/{repo} | Check team permissions for a repository (Legacy) |
| PUT | /teams/{team_id}/repos/{owner}/{repo} | Add or update team repository permissions (Legacy) |
| DELETE | /teams/{team_id}/repos/{owner}/{repo} | Remove a repository from a team (Legacy) |
| GET | /teams/{team_id}/teams | List child teams (Legacy) |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | Get the authenticated user |
| PATCH | /user | Update the authenticated user |
| GET | /user/emails | List email addresses for the authenticated user |
| POST | /user/emails | Add an email address for the authenticated user |
| DELETE | /user/emails | Delete an email address for the authenticated user |
| GET | /user/followers | List followers of the authenticated user |
| GET | /user/following | List the people the authenticated user follows |
| GET | /user/following/{username} | Check if a person is followed by the authenticated user |
| PUT | /user/following/{username} | Follow a user |
| DELETE | /user/following/{username} | Unfollow a user |
| GET | /user/gpg_keys | List GPG keys for the authenticated user |
| POST | /user/gpg_keys | Create a GPG key for the authenticated user |
| GET | /user/gpg_keys/{gpg_key_id} | Get a GPG key for the authenticated user |
| DELETE | /user/gpg_keys/{gpg_key_id} | Delete a GPG key for the authenticated user |
| GET | /user/installations | List app installations accessible to the user access token |
| GET | /user/installations/{installation_id}/repositories | List repositories accessible to the user access token |
| PUT | /user/installations/{installation_id}/repositories/{repository_id} | Add a repository to an app installation |
| DELETE | /user/installations/{installation_id}/repositories/{repository_id} | Remove a repository from an app installation |
| GET | /user/issues | List user account issues assigned to the authenticated user |
| GET | /user/keys | List public SSH keys for the authenticated user |
| POST | /user/keys | Create a public SSH key for the authenticated user |
| GET | /user/keys/{key_id} | Get a public SSH key for the authenticated user |
| DELETE | /user/keys/{key_id} | Delete a public SSH key for the authenticated user |
| GET | /user/memberships/orgs | List organization memberships for the authenticated user |
| GET | /user/memberships/orgs/{org} | Get an organization membership for the authenticated user |
| PATCH | /user/memberships/orgs/{org} | Update an organization membership for the authenticated user |
| GET | /user/orgs | List organizations for the authenticated user |
| POST | /user/projects | Create a user project |
| GET | /user/public_emails | List public email addresses for the authenticated user |
| GET | /user/repos | List repositories for the authenticated user |
| POST | /user/repos | Create a repository for the authenticated user |
| GET | /user/repository_invitations | List repository invitations for the authenticated user |
| PATCH | /user/repository_invitations/{invitation_id} | Accept a repository invitation |
| DELETE | /user/repository_invitations/{invitation_id} | Decline a repository invitation |
| GET | /user/starred | List repositories starred by the authenticated user |
| GET | /user/starred/{owner}/{repo} | Check if a repository is starred by the authenticated user |
| PUT | /user/starred/{owner}/{repo} | Star a repository for the authenticated user |
| DELETE | /user/starred/{owner}/{repo} | Unstar a repository for the authenticated user |
| GET | /user/subscriptions | List repositories watched by the authenticated user |
| GET | /user/teams | List teams for the authenticated user |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| GET | /users/{username} | Get a user |
| GET | /users/{username}/events | List events for the authenticated user |
| GET | /users/{username}/events/orgs/{org} | List organization events for the authenticated user |
| GET | /users/{username}/events/public | List public events for a user |
| GET | /users/{username}/followers | List followers of a user |
| GET | /users/{username}/following | List the people a user follows |
| GET | /users/{username}/following/{target_user} | Check if a user follows another user |
| GET | /users/{username}/gists | List gists for a user |
| GET | /users/{username}/gpg_keys | List GPG keys for a user |
| GET | /users/{username}/hovercard | Get contextual information for a user |
| GET | /users/{username}/installation | Get a user installation for the authenticated app |
| GET | /users/{username}/keys | List public keys for a user |
| GET | /users/{username}/orgs | List organizations for a user |
| GET | /users/{username}/projects | List user projects |
| GET | /users/{username}/received_events | List events received by the authenticated user |
| GET | /users/{username}/received_events/public | List public events received by a user |
| GET | /users/{username}/repos | List repositories for a user |
| PUT | /users/{username}/site_admin | Promote a user to be a site administrator |
| DELETE | /users/{username}/site_admin | Demote a site administrator |
| GET | /users/{username}/starred | List repositories starred by a user |
| GET | /users/{username}/subscriptions | List repositories watched by a user |
| PUT | /users/{username}/suspended | Suspend a user |
| DELETE | /users/{username}/suspended | Unsuspend a user |

### zen
| Method | Path | Description |
|--------|------|-------------|
| GET | /zen | Get the Zen of GitHub |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all hooks?" -> GET /admin/hooks
- "Create a hook?" -> POST /admin/hooks
- "Get hook details?" -> GET /admin/hooks/{hook_id}
- "Partially update a hook?" -> PATCH /admin/hooks/{hook_id}
- "Delete a hook?" -> DELETE /admin/hooks/{hook_id}
- "Create a ping?" -> POST /admin/hooks/{hook_id}/pings
- "List all keys?" -> GET /admin/keys
- "Delete a key?" -> DELETE /admin/keys/{key_ids}
- "Create a sync?" -> POST /admin/ldap/teams/{team_id}/sync
- "Create a sync?" -> POST /admin/ldap/users/{username}/sync
- "Create a organization?" -> POST /admin/organizations
- "Partially update a organization?" -> PATCH /admin/organizations/{org}
- "List all pre-receive-environments?" -> GET /admin/pre-receive-environments
- "Create a pre-receive-environment?" -> POST /admin/pre-receive-environments
- "Get pre-receive-environment details?" -> GET /admin/pre-receive-environments/{pre_receive_environment_id}
- "Partially update a pre-receive-environment?" -> PATCH /admin/pre-receive-environments/{pre_receive_environment_id}
- "Delete a pre-receive-environment?" -> DELETE /admin/pre-receive-environments/{pre_receive_environment_id}
- "Create a download?" -> POST /admin/pre-receive-environments/{pre_receive_environment_id}/downloads
- "List all latest?" -> GET /admin/pre-receive-environments/{pre_receive_environment_id}/downloads/latest
- "List all pre-receive-hooks?" -> GET /admin/pre-receive-hooks
- "Create a pre-receive-hook?" -> POST /admin/pre-receive-hooks
- "Get pre-receive-hook details?" -> GET /admin/pre-receive-hooks/{pre_receive_hook_id}
- "Partially update a pre-receive-hook?" -> PATCH /admin/pre-receive-hooks/{pre_receive_hook_id}
- "Delete a pre-receive-hook?" -> DELETE /admin/pre-receive-hooks/{pre_receive_hook_id}
- "List all tokens?" -> GET /admin/tokens
- "Delete a token?" -> DELETE /admin/tokens/{token_id}
- "Create a user?" -> POST /admin/users
- "Partially update a user?" -> PATCH /admin/users/{username}
- "Delete a user?" -> DELETE /admin/users/{username}
- "Create a authorization?" -> POST /admin/users/{username}/authorizations
- "List all app?" -> GET /app
- "Create a conversion?" -> POST /app-manifests/{code}/conversions
- "List all config?" -> GET /app/hook/config
- "List all deliveries?" -> GET /app/hook/deliveries
- "Get delivery details?" -> GET /app/hook/deliveries/{delivery_id}
- "Create a attempt?" -> POST /app/hook/deliveries/{delivery_id}/attempts
- "List all installations?" -> GET /app/installations
- "Get installation details?" -> GET /app/installations/{installation_id}
- "Delete a installation?" -> DELETE /app/installations/{installation_id}
- "Create a access_token?" -> POST /app/installations/{installation_id}/access_tokens
- "List all grants?" -> GET /applications/grants
- "Get grant details?" -> GET /applications/grants/{grant_id}
- "Delete a grant?" -> DELETE /applications/grants/{grant_id}
- "Delete a grant?" -> DELETE /applications/{client_id}/grants/{access_token}
- "Create a token?" -> POST /applications/{client_id}/token
- "Create a scoped?" -> POST /applications/{client_id}/token/scoped
- "Get token details?" -> GET /applications/{client_id}/tokens/{access_token}
- "Delete a token?" -> DELETE /applications/{client_id}/tokens/{access_token}
- "Get app details?" -> GET /apps/{app_slug}
- "List all authorizations?" -> GET /authorizations
- "Create a authorization?" -> POST /authorizations
- "Update a client?" -> PUT /authorizations/clients/{client_id}
- "Update a client?" -> PUT /authorizations/clients/{client_id}/{fingerprint}
- "Get authorization details?" -> GET /authorizations/{authorization_id}
- "Partially update a authorization?" -> PATCH /authorizations/{authorization_id}
- "Delete a authorization?" -> DELETE /authorizations/{authorization_id}
- "List all codes_of_conduct?" -> GET /codes_of_conduct
- "Get codes_of_conduct details?" -> GET /codes_of_conduct/{key}
- "List all emojis?" -> GET /emojis
- "List all announcement?" -> GET /enterprise/announcement
- "List all license?" -> GET /enterprise/settings/license
- "List all all?" -> GET /enterprise/stats/all
- "List all comments?" -> GET /enterprise/stats/comments
- "List all gists?" -> GET /enterprise/stats/gists
- "List all hooks?" -> GET /enterprise/stats/hooks
- "List all issues?" -> GET /enterprise/stats/issues
- "List all milestones?" -> GET /enterprise/stats/milestones
- "List all orgs?" -> GET /enterprise/stats/orgs
- "List all pages?" -> GET /enterprise/stats/pages
- "List all pulls?" -> GET /enterprise/stats/pulls
- "List all repos?" -> GET /enterprise/stats/repos
- "List all users?" -> GET /enterprise/stats/users
- "List all permissions?" -> GET /enterprises/{enterprise}/actions/permissions
- "List all organizations?" -> GET /enterprises/{enterprise}/actions/permissions/organizations
- "Update a organization?" -> PUT /enterprises/{enterprise}/actions/permissions/organizations/{org_id}
- "Delete a organization?" -> DELETE /enterprises/{enterprise}/actions/permissions/organizations/{org_id}
- "List all selected-actions?" -> GET /enterprises/{enterprise}/actions/permissions/selected-actions
- "List all runner-groups?" -> GET /enterprises/{enterprise}/actions/runner-groups
- "Create a runner-group?" -> POST /enterprises/{enterprise}/actions/runner-groups
- "Get runner-group details?" -> GET /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}
- "Partially update a runner-group?" -> PATCH /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}
- "Delete a runner-group?" -> DELETE /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}
- "List all organizations?" -> GET /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations
- "Update a organization?" -> PUT /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations/{org_id}
- "Delete a organization?" -> DELETE /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/organizations/{org_id}
- "List all runners?" -> GET /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners
- "Update a runner?" -> PUT /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "Delete a runner?" -> DELETE /enterprises/{enterprise}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "List all runners?" -> GET /enterprises/{enterprise}/actions/runners
- "List all downloads?" -> GET /enterprises/{enterprise}/actions/runners/downloads
- "Create a registration-token?" -> POST /enterprises/{enterprise}/actions/runners/registration-token
- "Create a remove-token?" -> POST /enterprises/{enterprise}/actions/runners/remove-token
- "Get runner details?" -> GET /enterprises/{enterprise}/actions/runners/{runner_id}
- "Delete a runner?" -> DELETE /enterprises/{enterprise}/actions/runners/{runner_id}
- "List all audit-log?" -> GET /enterprises/{enterprise}/audit-log
- "List all events?" -> GET /events
- "List all feeds?" -> GET /feeds
- "List all gists?" -> GET /gists
- "Create a gist?" -> POST /gists
- "List all public?" -> GET /gists/public
- "List all starred?" -> GET /gists/starred
- "Get gist details?" -> GET /gists/{gist_id}
- "Partially update a gist?" -> PATCH /gists/{gist_id}
- "Delete a gist?" -> DELETE /gists/{gist_id}
- "List all comments?" -> GET /gists/{gist_id}/comments
- "Create a comment?" -> POST /gists/{gist_id}/comments
- "Get comment details?" -> GET /gists/{gist_id}/comments/{comment_id}
- "Partially update a comment?" -> PATCH /gists/{gist_id}/comments/{comment_id}
- "Delete a comment?" -> DELETE /gists/{gist_id}/comments/{comment_id}
- "List all commits?" -> GET /gists/{gist_id}/commits
- "List all forks?" -> GET /gists/{gist_id}/forks
- "Create a fork?" -> POST /gists/{gist_id}/forks
- "List all star?" -> GET /gists/{gist_id}/star
- "Get gist details?" -> GET /gists/{gist_id}/{sha}
- "List all templates?" -> GET /gitignore/templates
- "Get template details?" -> GET /gitignore/templates/{name}
- "List all repositories?" -> GET /installation/repositories
- "List all issues?" -> GET /issues
- "List all licenses?" -> GET /licenses
- "Get license details?" -> GET /licenses/{license}
- "Create a markdown?" -> POST /markdown
- "Create a raw?" -> POST /markdown/raw
- "List all meta?" -> GET /meta
- "List all events?" -> GET /networks/{owner}/{repo}/events
- "List all notifications?" -> GET /notifications
- "Get thread details?" -> GET /notifications/threads/{thread_id}
- "Partially update a thread?" -> PATCH /notifications/threads/{thread_id}
- "List all subscription?" -> GET /notifications/threads/{thread_id}/subscription
- "List all octocat?" -> GET /octocat
- "List all organizations?" -> GET /organizations
- "Get org details?" -> GET /orgs/{org}
- "Partially update a org?" -> PATCH /orgs/{org}
- "List all permissions?" -> GET /orgs/{org}/actions/permissions
- "List all repositories?" -> GET /orgs/{org}/actions/permissions/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/permissions/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/permissions/repositories/{repository_id}
- "List all selected-actions?" -> GET /orgs/{org}/actions/permissions/selected-actions
- "List all runner-groups?" -> GET /orgs/{org}/actions/runner-groups
- "Create a runner-group?" -> POST /orgs/{org}/actions/runner-groups
- "Get runner-group details?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}
- "Partially update a runner-group?" -> PATCH /orgs/{org}/actions/runner-groups/{runner_group_id}
- "Delete a runner-group?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}
- "List all repositories?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}/repositories/{repository_id}
- "List all runners?" -> GET /orgs/{org}/actions/runner-groups/{runner_group_id}/runners
- "Update a runner?" -> PUT /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "Delete a runner?" -> DELETE /orgs/{org}/actions/runner-groups/{runner_group_id}/runners/{runner_id}
- "List all runners?" -> GET /orgs/{org}/actions/runners
- "List all downloads?" -> GET /orgs/{org}/actions/runners/downloads
- "Create a registration-token?" -> POST /orgs/{org}/actions/runners/registration-token
- "Create a remove-token?" -> POST /orgs/{org}/actions/runners/remove-token
- "Get runner details?" -> GET /orgs/{org}/actions/runners/{runner_id}
- "Delete a runner?" -> DELETE /orgs/{org}/actions/runners/{runner_id}
- "List all secrets?" -> GET /orgs/{org}/actions/secrets
- "List all public-key?" -> GET /orgs/{org}/actions/secrets/public-key
- "Get secret details?" -> GET /orgs/{org}/actions/secrets/{secret_name}
- "Update a secret?" -> PUT /orgs/{org}/actions/secrets/{secret_name}
- "Delete a secret?" -> DELETE /orgs/{org}/actions/secrets/{secret_name}
- "List all repositories?" -> GET /orgs/{org}/actions/secrets/{secret_name}/repositories
- "Update a repository?" -> PUT /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}
- "List all audit-log?" -> GET /orgs/{org}/audit-log
- "List all events?" -> GET /orgs/{org}/events
- "List all hooks?" -> GET /orgs/{org}/hooks
- "Create a hook?" -> POST /orgs/{org}/hooks
- "Get hook details?" -> GET /orgs/{org}/hooks/{hook_id}
- "Partially update a hook?" -> PATCH /orgs/{org}/hooks/{hook_id}
- "Delete a hook?" -> DELETE /orgs/{org}/hooks/{hook_id}
- "List all config?" -> GET /orgs/{org}/hooks/{hook_id}/config
- "List all deliveries?" -> GET /orgs/{org}/hooks/{hook_id}/deliveries
- "Get delivery details?" -> GET /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}
- "Create a attempt?" -> POST /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}/attempts
- "Create a ping?" -> POST /orgs/{org}/hooks/{hook_id}/pings
- "List all installation?" -> GET /orgs/{org}/installation
- "List all installations?" -> GET /orgs/{org}/installations
- "List all issues?" -> GET /orgs/{org}/issues
- "List all members?" -> GET /orgs/{org}/members
- "Get member details?" -> GET /orgs/{org}/members/{username}
- "Delete a member?" -> DELETE /orgs/{org}/members/{username}
- "Get membership details?" -> GET /orgs/{org}/memberships/{username}
- "Update a membership?" -> PUT /orgs/{org}/memberships/{username}
- "Delete a membership?" -> DELETE /orgs/{org}/memberships/{username}
- "List all outside_collaborators?" -> GET /orgs/{org}/outside_collaborators
- "Update a outside_collaborator?" -> PUT /orgs/{org}/outside_collaborators/{username}
- "Delete a outside_collaborator?" -> DELETE /orgs/{org}/outside_collaborators/{username}
- "List all pre-receive-hooks?" -> GET /orgs/{org}/pre-receive-hooks
- "Get pre-receive-hook details?" -> GET /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id}
- "Partially update a pre-receive-hook?" -> PATCH /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id}
- "Delete a pre-receive-hook?" -> DELETE /orgs/{org}/pre-receive-hooks/{pre_receive_hook_id}
- "List all projects?" -> GET /orgs/{org}/projects
- "Create a project?" -> POST /orgs/{org}/projects
- "List all public_members?" -> GET /orgs/{org}/public_members
- "Get public_member details?" -> GET /orgs/{org}/public_members/{username}
- "Update a public_member?" -> PUT /orgs/{org}/public_members/{username}
- "Delete a public_member?" -> DELETE /orgs/{org}/public_members/{username}
- "List all repos?" -> GET /orgs/{org}/repos
- "Create a repo?" -> POST /orgs/{org}/repos
- "List all alerts?" -> GET /orgs/{org}/secret-scanning/alerts
- "List all teams?" -> GET /orgs/{org}/teams
- "Create a team?" -> POST /orgs/{org}/teams
- "Get team details?" -> GET /orgs/{org}/teams/{team_slug}
- "Partially update a team?" -> PATCH /orgs/{org}/teams/{team_slug}
- "Delete a team?" -> DELETE /orgs/{org}/teams/{team_slug}
- "List all discussions?" -> GET /orgs/{org}/teams/{team_slug}/discussions
- "Create a discussion?" -> POST /orgs/{org}/teams/{team_slug}/discussions
- "Get discussion details?" -> GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}
- "Partially update a discussion?" -> PATCH /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}
- "Delete a discussion?" -> DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}
- "List all comments?" -> GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments
- "Create a comment?" -> POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments
- "Get comment details?" -> GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}
- "Partially update a comment?" -> PATCH /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}
- "Delete a comment?" -> DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}
- "List all reactions?" -> GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions
- "Create a reaction?" -> POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions
- "Delete a reaction?" -> DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions/{reaction_id}
- "List all reactions?" -> GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions
- "Create a reaction?" -> POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions
- "Delete a reaction?" -> DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions/{reaction_id}
- "List all members?" -> GET /orgs/{org}/teams/{team_slug}/members
- "Get membership details?" -> GET /orgs/{org}/teams/{team_slug}/memberships/{username}
- "Update a membership?" -> PUT /orgs/{org}/teams/{team_slug}/memberships/{username}
- "Delete a membership?" -> DELETE /orgs/{org}/teams/{team_slug}/memberships/{username}
- "List all projects?" -> GET /orgs/{org}/teams/{team_slug}/projects
- "Get project details?" -> GET /orgs/{org}/teams/{team_slug}/projects/{project_id}
- "Update a project?" -> PUT /orgs/{org}/teams/{team_slug}/projects/{project_id}
- "Delete a project?" -> DELETE /orgs/{org}/teams/{team_slug}/projects/{project_id}
- "List all repos?" -> GET /orgs/{org}/teams/{team_slug}/repos
- "Get repo details?" -> GET /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "Update a repo?" -> PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
- "List all teams?" -> GET /orgs/{org}/teams/{team_slug}/teams
- "Get card details?" -> GET /projects/columns/cards/{card_id}
- "Partially update a card?" -> PATCH /projects/columns/cards/{card_id}
- "Delete a card?" -> DELETE /projects/columns/cards/{card_id}
- "Create a move?" -> POST /projects/columns/cards/{card_id}/moves
- "Get column details?" -> GET /projects/columns/{column_id}
- "Partially update a column?" -> PATCH /projects/columns/{column_id}
- "Delete a column?" -> DELETE /projects/columns/{column_id}
- "List all cards?" -> GET /projects/columns/{column_id}/cards
- "Create a card?" -> POST /projects/columns/{column_id}/cards
- "Create a move?" -> POST /projects/columns/{column_id}/moves
- "Get project details?" -> GET /projects/{project_id}
- "Partially update a project?" -> PATCH /projects/{project_id}
- "Delete a project?" -> DELETE /projects/{project_id}
- "List all collaborators?" -> GET /projects/{project_id}/collaborators
- "Update a collaborator?" -> PUT /projects/{project_id}/collaborators/{username}
- "Delete a collaborator?" -> DELETE /projects/{project_id}/collaborators/{username}
- "List all permission?" -> GET /projects/{project_id}/collaborators/{username}/permission
- "List all columns?" -> GET /projects/{project_id}/columns
- "Create a column?" -> POST /projects/{project_id}/columns
- "List all rate_limit?" -> GET /rate_limit
- "Delete a reaction?" -> DELETE /reactions/{reaction_id}
- "Get repo details?" -> GET /repos/{owner}/{repo}
- "Partially update a repo?" -> PATCH /repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /repos/{owner}/{repo}
- "List all artifacts?" -> GET /repos/{owner}/{repo}/actions/artifacts
- "Get artifact details?" -> GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}
- "Delete a artifact?" -> DELETE /repos/{owner}/{repo}/actions/artifacts/{artifact_id}
- "Get artifact details?" -> GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format}
- "Get job details?" -> GET /repos/{owner}/{repo}/actions/jobs/{job_id}
- "List all logs?" -> GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs
- "List all permissions?" -> GET /repos/{owner}/{repo}/actions/permissions
- "List all selected-actions?" -> GET /repos/{owner}/{repo}/actions/permissions/selected-actions
- "List all runners?" -> GET /repos/{owner}/{repo}/actions/runners
- "List all downloads?" -> GET /repos/{owner}/{repo}/actions/runners/downloads
- "Create a registration-token?" -> POST /repos/{owner}/{repo}/actions/runners/registration-token
- "Create a remove-token?" -> POST /repos/{owner}/{repo}/actions/runners/remove-token
- "Get runner details?" -> GET /repos/{owner}/{repo}/actions/runners/{runner_id}
- "Delete a runner?" -> DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}
- "List all runs?" -> GET /repos/{owner}/{repo}/actions/runs
- "Get run details?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}
- "Delete a run?" -> DELETE /repos/{owner}/{repo}/actions/runs/{run_id}
- "List all approvals?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/approvals
- "List all artifacts?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts
- "Create a cancel?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel
- "List all jobs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
- "List all logs?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs
- "List all pending_deployments?" -> GET /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments
- "Create a pending_deployment?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/pending_deployments
- "Create a rerun?" -> POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun
- "List all secrets?" -> GET /repos/{owner}/{repo}/actions/secrets
- "List all public-key?" -> GET /repos/{owner}/{repo}/actions/secrets/public-key
- "Get secret details?" -> GET /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "Update a secret?" -> PUT /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repos/{owner}/{repo}/actions/secrets/{secret_name}
- "List all workflows?" -> GET /repos/{owner}/{repo}/actions/workflows
- "Get workflow details?" -> GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}
- "Create a dispatche?" -> POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
- "List all runs?" -> GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs
- "List all assignees?" -> GET /repos/{owner}/{repo}/assignees
- "Get assignee details?" -> GET /repos/{owner}/{repo}/assignees/{assignee}
- "List all autolinks?" -> GET /repos/{owner}/{repo}/autolinks
- "Create a autolink?" -> POST /repos/{owner}/{repo}/autolinks
- "Get autolink details?" -> GET /repos/{owner}/{repo}/autolinks/{autolink_id}
- "Delete a autolink?" -> DELETE /repos/{owner}/{repo}/autolinks/{autolink_id}
- "List all branches?" -> GET /repos/{owner}/{repo}/branches
- "Get branche details?" -> GET /repos/{owner}/{repo}/branches/{branch}
- "List all protection?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection
- "List all enforce_admins?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins
- "Create a enforce_admin?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins
- "List all required_pull_request_reviews?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews
- "List all required_signatures?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures
- "Create a required_signature?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/required_signatures
- "List all required_status_checks?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks
- "List all contexts?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts
- "Create a context?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts
- "List all restrictions?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions
- "List all apps?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps
- "Create a app?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/apps
- "List all teams?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams
- "Create a team?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams
- "List all users?" -> GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users
- "Create a user?" -> POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users
- "Create a rename?" -> POST /repos/{owner}/{repo}/branches/{branch}/rename
- "Create a check-run?" -> POST /repos/{owner}/{repo}/check-runs
- "Get check-run details?" -> GET /repos/{owner}/{repo}/check-runs/{check_run_id}
- "Partially update a check-run?" -> PATCH /repos/{owner}/{repo}/check-runs/{check_run_id}
- "List all annotations?" -> GET /repos/{owner}/{repo}/check-runs/{check_run_id}/annotations
- "Create a rerequest?" -> POST /repos/{owner}/{repo}/check-runs/{check_run_id}/rerequest
- "Create a check-suite?" -> POST /repos/{owner}/{repo}/check-suites
- "Get check-suite details?" -> GET /repos/{owner}/{repo}/check-suites/{check_suite_id}
- "List all check-runs?" -> GET /repos/{owner}/{repo}/check-suites/{check_suite_id}/check-runs
- "Create a rerequest?" -> POST /repos/{owner}/{repo}/check-suites/{check_suite_id}/rerequest
- "List all alerts?" -> GET /repos/{owner}/{repo}/code-scanning/alerts
- "Get alert details?" -> GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}
- "Partially update a alert?" -> PATCH /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}
- "List all instances?" -> GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/instances
- "List all analyses?" -> GET /repos/{owner}/{repo}/code-scanning/analyses
- "Get analysis details?" -> GET /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}
- "Delete a analysis?" -> DELETE /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}
- "Create a sarif?" -> POST /repos/{owner}/{repo}/code-scanning/sarifs
- "Get sarif details?" -> GET /repos/{owner}/{repo}/code-scanning/sarifs/{sarif_id}
- "List all collaborators?" -> GET /repos/{owner}/{repo}/collaborators
- "Get collaborator details?" -> GET /repos/{owner}/{repo}/collaborators/{username}
- "Update a collaborator?" -> PUT /repos/{owner}/{repo}/collaborators/{username}
- "Delete a collaborator?" -> DELETE /repos/{owner}/{repo}/collaborators/{username}
- "List all permission?" -> GET /repos/{owner}/{repo}/collaborators/{username}/permission
- "List all comments?" -> GET /repos/{owner}/{repo}/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/comments/{comment_id}/reactions/{reaction_id}
- "List all commits?" -> GET /repos/{owner}/{repo}/commits
- "List all branches-where-head?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/branches-where-head
- "List all comments?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/commits/{commit_sha}/comments
- "List all pulls?" -> GET /repos/{owner}/{repo}/commits/{commit_sha}/pulls
- "Get commit details?" -> GET /repos/{owner}/{repo}/commits/{ref}
- "List all check-runs?" -> GET /repos/{owner}/{repo}/commits/{ref}/check-runs
- "List all check-suites?" -> GET /repos/{owner}/{repo}/commits/{ref}/check-suites
- "List all status?" -> GET /repos/{owner}/{repo}/commits/{ref}/status
- "List all statuses?" -> GET /repos/{owner}/{repo}/commits/{ref}/statuses
- "Get compare details?" -> GET /repos/{owner}/{repo}/compare/{basehead}
- "Create a attachment?" -> POST /repos/{owner}/{repo}/content_references/{content_reference_id}/attachments
- "Get content details?" -> GET /repos/{owner}/{repo}/contents/{path}
- "Update a content?" -> PUT /repos/{owner}/{repo}/contents/{path}
- "Delete a content?" -> DELETE /repos/{owner}/{repo}/contents/{path}
- "List all contributors?" -> GET /repos/{owner}/{repo}/contributors
- "List all deployments?" -> GET /repos/{owner}/{repo}/deployments
- "Create a deployment?" -> POST /repos/{owner}/{repo}/deployments
- "Get deployment details?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}
- "Delete a deployment?" -> DELETE /repos/{owner}/{repo}/deployments/{deployment_id}
- "List all statuses?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses
- "Create a statuse?" -> POST /repos/{owner}/{repo}/deployments/{deployment_id}/statuses
- "Get statuse details?" -> GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id}
- "Create a dispatche?" -> POST /repos/{owner}/{repo}/dispatches
- "List all environments?" -> GET /repos/{owner}/{repo}/environments
- "Get environment details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}
- "Update a environment?" -> PUT /repos/{owner}/{repo}/environments/{environment_name}
- "Delete a environment?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}
- "List all deployment-branch-policies?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies
- "Create a deployment-branch-policy?" -> POST /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies
- "Get deployment-branch-policy details?" -> GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "Update a deployment-branch-policy?" -> PUT /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "Delete a deployment-branch-policy?" -> DELETE /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}
- "List all events?" -> GET /repos/{owner}/{repo}/events
- "List all forks?" -> GET /repos/{owner}/{repo}/forks
- "Create a fork?" -> POST /repos/{owner}/{repo}/forks
- "Create a blob?" -> POST /repos/{owner}/{repo}/git/blobs
- "Get blob details?" -> GET /repos/{owner}/{repo}/git/blobs/{file_sha}
- "Create a commit?" -> POST /repos/{owner}/{repo}/git/commits
- "Get commit details?" -> GET /repos/{owner}/{repo}/git/commits/{commit_sha}
- "Get matching-ref details?" -> GET /repos/{owner}/{repo}/git/matching-refs/{ref}
- "Get ref details?" -> GET /repos/{owner}/{repo}/git/ref/{ref}
- "Create a ref?" -> POST /repos/{owner}/{repo}/git/refs
- "Partially update a ref?" -> PATCH /repos/{owner}/{repo}/git/refs/{ref}
- "Delete a ref?" -> DELETE /repos/{owner}/{repo}/git/refs/{ref}
- "Create a tag?" -> POST /repos/{owner}/{repo}/git/tags
- "Get tag details?" -> GET /repos/{owner}/{repo}/git/tags/{tag_sha}
- "Create a tree?" -> POST /repos/{owner}/{repo}/git/trees
- "Get tree details?" -> GET /repos/{owner}/{repo}/git/trees/{tree_sha}
- "List all hooks?" -> GET /repos/{owner}/{repo}/hooks
- "Create a hook?" -> POST /repos/{owner}/{repo}/hooks
- "Get hook details?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}
- "Partially update a hook?" -> PATCH /repos/{owner}/{repo}/hooks/{hook_id}
- "Delete a hook?" -> DELETE /repos/{owner}/{repo}/hooks/{hook_id}
- "List all config?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/config
- "List all deliveries?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/deliveries
- "Get delivery details?" -> GET /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}
- "Create a attempt?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts
- "Create a ping?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/pings
- "Create a test?" -> POST /repos/{owner}/{repo}/hooks/{hook_id}/tests
- "List all installation?" -> GET /repos/{owner}/{repo}/installation
- "List all invitations?" -> GET /repos/{owner}/{repo}/invitations
- "Partially update a invitation?" -> PATCH /repos/{owner}/{repo}/invitations/{invitation_id}
- "Delete a invitation?" -> DELETE /repos/{owner}/{repo}/invitations/{invitation_id}
- "List all issues?" -> GET /repos/{owner}/{repo}/issues
- "Create a issue?" -> POST /repos/{owner}/{repo}/issues
- "List all comments?" -> GET /repos/{owner}/{repo}/issues/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/issues/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/issues/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}
- "List all events?" -> GET /repos/{owner}/{repo}/issues/events
- "Get event details?" -> GET /repos/{owner}/{repo}/issues/events/{event_id}
- "Get issue details?" -> GET /repos/{owner}/{repo}/issues/{issue_number}
- "Partially update a issue?" -> PATCH /repos/{owner}/{repo}/issues/{issue_number}
- "Create a assignee?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/assignees
- "Get assignee details?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/assignees/{assignee}
- "List all comments?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/comments
- "List all events?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/events
- "List all labels?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/labels
- "Create a label?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/labels
- "Delete a label?" -> DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}
- "List all reactions?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/issues/{issue_number}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id}
- "List all timeline?" -> GET /repos/{owner}/{repo}/issues/{issue_number}/timeline
- "List all keys?" -> GET /repos/{owner}/{repo}/keys
- "Create a key?" -> POST /repos/{owner}/{repo}/keys
- "Get key details?" -> GET /repos/{owner}/{repo}/keys/{key_id}
- "Delete a key?" -> DELETE /repos/{owner}/{repo}/keys/{key_id}
- "List all labels?" -> GET /repos/{owner}/{repo}/labels
- "Create a label?" -> POST /repos/{owner}/{repo}/labels
- "Get label details?" -> GET /repos/{owner}/{repo}/labels/{name}
- "Partially update a label?" -> PATCH /repos/{owner}/{repo}/labels/{name}
- "Delete a label?" -> DELETE /repos/{owner}/{repo}/labels/{name}
- "List all languages?" -> GET /repos/{owner}/{repo}/languages
- "List all license?" -> GET /repos/{owner}/{repo}/license
- "Create a merge-upstream?" -> POST /repos/{owner}/{repo}/merge-upstream
- "Create a merge?" -> POST /repos/{owner}/{repo}/merges
- "List all milestones?" -> GET /repos/{owner}/{repo}/milestones
- "Create a milestone?" -> POST /repos/{owner}/{repo}/milestones
- "Get milestone details?" -> GET /repos/{owner}/{repo}/milestones/{milestone_number}
- "Partially update a milestone?" -> PATCH /repos/{owner}/{repo}/milestones/{milestone_number}
- "Delete a milestone?" -> DELETE /repos/{owner}/{repo}/milestones/{milestone_number}
- "List all labels?" -> GET /repos/{owner}/{repo}/milestones/{milestone_number}/labels
- "List all notifications?" -> GET /repos/{owner}/{repo}/notifications
- "List all pages?" -> GET /repos/{owner}/{repo}/pages
- "Create a page?" -> POST /repos/{owner}/{repo}/pages
- "List all builds?" -> GET /repos/{owner}/{repo}/pages/builds
- "Create a build?" -> POST /repos/{owner}/{repo}/pages/builds
- "List all latest?" -> GET /repos/{owner}/{repo}/pages/builds/latest
- "Get build details?" -> GET /repos/{owner}/{repo}/pages/builds/{build_id}
- "List all pre-receive-hooks?" -> GET /repos/{owner}/{repo}/pre-receive-hooks
- "Get pre-receive-hook details?" -> GET /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id}
- "Partially update a pre-receive-hook?" -> PATCH /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id}
- "Delete a pre-receive-hook?" -> DELETE /repos/{owner}/{repo}/pre-receive-hooks/{pre_receive_hook_id}
- "List all projects?" -> GET /repos/{owner}/{repo}/projects
- "Create a project?" -> POST /repos/{owner}/{repo}/projects
- "List all pulls?" -> GET /repos/{owner}/{repo}/pulls
- "Create a pull?" -> POST /repos/{owner}/{repo}/pulls
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/comments
- "Get comment details?" -> GET /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "Partially update a comment?" -> PATCH /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "Delete a comment?" -> DELETE /repos/{owner}/{repo}/pulls/comments/{comment_id}
- "List all reactions?" -> GET /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions/{reaction_id}
- "Get pull details?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}
- "Partially update a pull?" -> PATCH /repos/{owner}/{repo}/pulls/{pull_number}
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/comments
- "Create a comment?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/comments
- "Create a reply?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies
- "List all commits?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/commits
- "List all files?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/files
- "List all merge?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/merge
- "List all requested_reviewers?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers
- "Create a requested_reviewer?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers
- "List all reviews?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
- "Create a review?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
- "Get review details?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "Update a review?" -> PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "Delete a review?" -> DELETE /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
- "List all comments?" -> GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/comments
- "Create a event?" -> POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events
- "List all readme?" -> GET /repos/{owner}/{repo}/readme
- "Get readme details?" -> GET /repos/{owner}/{repo}/readme/{dir}
- "List all releases?" -> GET /repos/{owner}/{repo}/releases
- "Create a release?" -> POST /repos/{owner}/{repo}/releases
- "Get asset details?" -> GET /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Partially update a asset?" -> PATCH /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Delete a asset?" -> DELETE /repos/{owner}/{repo}/releases/assets/{asset_id}
- "Create a generate-note?" -> POST /repos/{owner}/{repo}/releases/generate-notes
- "List all latest?" -> GET /repos/{owner}/{repo}/releases/latest
- "Get tag details?" -> GET /repos/{owner}/{repo}/releases/tags/{tag}
- "Get release details?" -> GET /repos/{owner}/{repo}/releases/{release_id}
- "Partially update a release?" -> PATCH /repos/{owner}/{repo}/releases/{release_id}
- "Delete a release?" -> DELETE /repos/{owner}/{repo}/releases/{release_id}
- "List all assets?" -> GET /repos/{owner}/{repo}/releases/{release_id}/assets
- "Create a asset?" -> POST /repos/{owner}/{repo}/releases/{release_id}/assets
- "List all reactions?" -> GET /repos/{owner}/{repo}/releases/{release_id}/reactions
- "Create a reaction?" -> POST /repos/{owner}/{repo}/releases/{release_id}/reactions
- "Delete a reaction?" -> DELETE /repos/{owner}/{repo}/releases/{release_id}/reactions/{reaction_id}
- "List all alerts?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts
- "Get alert details?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
- "Partially update a alert?" -> PATCH /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
- "List all locations?" -> GET /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}/locations
- "List all stargazers?" -> GET /repos/{owner}/{repo}/stargazers
- "List all code_frequency?" -> GET /repos/{owner}/{repo}/stats/code_frequency
- "List all commit_activity?" -> GET /repos/{owner}/{repo}/stats/commit_activity
- "List all contributors?" -> GET /repos/{owner}/{repo}/stats/contributors
- "List all participation?" -> GET /repos/{owner}/{repo}/stats/participation
- "List all punch_card?" -> GET /repos/{owner}/{repo}/stats/punch_card
- "List all subscribers?" -> GET /repos/{owner}/{repo}/subscribers
- "List all subscription?" -> GET /repos/{owner}/{repo}/subscription
- "List all tags?" -> GET /repos/{owner}/{repo}/tags
- "Get tarball details?" -> GET /repos/{owner}/{repo}/tarball/{ref}
- "List all teams?" -> GET /repos/{owner}/{repo}/teams
- "List all topics?" -> GET /repos/{owner}/{repo}/topics
- "Create a transfer?" -> POST /repos/{owner}/{repo}/transfer
- "Get zipball details?" -> GET /repos/{owner}/{repo}/zipball/{ref}
- "Create a generate?" -> POST /repos/{template_owner}/{template_repo}/generate
- "List all repositories?" -> GET /repositories
- "List all secrets?" -> GET /repositories/{repository_id}/environments/{environment_name}/secrets
- "List all public-key?" -> GET /repositories/{repository_id}/environments/{environment_name}/secrets/public-key
- "Get secret details?" -> GET /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}
- "Update a secret?" -> PUT /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}
- "Delete a secret?" -> DELETE /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}
- "Search code?" -> GET /search/code
- "Search commits?" -> GET /search/commits
- "Search issues?" -> GET /search/issues
- "Search labels?" -> GET /search/labels
- "Search repositories?" -> GET /search/repositories
- "Search topics?" -> GET /search/topics
- "Search users?" -> GET /search/users
- "List all configcheck?" -> GET /setup/api/configcheck
- "Create a configure?" -> POST /setup/api/configure
- "List all maintenance?" -> GET /setup/api/maintenance
- "Create a maintenance?" -> POST /setup/api/maintenance
- "List all settings?" -> GET /setup/api/settings
- "List all authorized-keys?" -> GET /setup/api/settings/authorized-keys
- "Create a authorized-key?" -> POST /setup/api/settings/authorized-keys
- "Create a start?" -> POST /setup/api/start
- "Create a upgrade?" -> POST /setup/api/upgrade
- "Get team details?" -> GET /teams/{team_id}
- "Partially update a team?" -> PATCH /teams/{team_id}
- "Delete a team?" -> DELETE /teams/{team_id}
- "List all discussions?" -> GET /teams/{team_id}/discussions
- "Create a discussion?" -> POST /teams/{team_id}/discussions
- "Get discussion details?" -> GET /teams/{team_id}/discussions/{discussion_number}
- "Partially update a discussion?" -> PATCH /teams/{team_id}/discussions/{discussion_number}
- "Delete a discussion?" -> DELETE /teams/{team_id}/discussions/{discussion_number}
- "List all comments?" -> GET /teams/{team_id}/discussions/{discussion_number}/comments
- "Create a comment?" -> POST /teams/{team_id}/discussions/{discussion_number}/comments
- "Get comment details?" -> GET /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}
- "Partially update a comment?" -> PATCH /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}
- "Delete a comment?" -> DELETE /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}
- "List all reactions?" -> GET /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions
- "Create a reaction?" -> POST /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions
- "List all reactions?" -> GET /teams/{team_id}/discussions/{discussion_number}/reactions
- "Create a reaction?" -> POST /teams/{team_id}/discussions/{discussion_number}/reactions
- "List all members?" -> GET /teams/{team_id}/members
- "Get member details?" -> GET /teams/{team_id}/members/{username}
- "Update a member?" -> PUT /teams/{team_id}/members/{username}
- "Delete a member?" -> DELETE /teams/{team_id}/members/{username}
- "Get membership details?" -> GET /teams/{team_id}/memberships/{username}
- "Update a membership?" -> PUT /teams/{team_id}/memberships/{username}
- "Delete a membership?" -> DELETE /teams/{team_id}/memberships/{username}
- "List all projects?" -> GET /teams/{team_id}/projects
- "Get project details?" -> GET /teams/{team_id}/projects/{project_id}
- "Update a project?" -> PUT /teams/{team_id}/projects/{project_id}
- "Delete a project?" -> DELETE /teams/{team_id}/projects/{project_id}
- "List all repos?" -> GET /teams/{team_id}/repos
- "Get repo details?" -> GET /teams/{team_id}/repos/{owner}/{repo}
- "Update a repo?" -> PUT /teams/{team_id}/repos/{owner}/{repo}
- "Delete a repo?" -> DELETE /teams/{team_id}/repos/{owner}/{repo}
- "List all teams?" -> GET /teams/{team_id}/teams
- "List all user?" -> GET /user
- "List all emails?" -> GET /user/emails
- "Create a email?" -> POST /user/emails
- "List all followers?" -> GET /user/followers
- "List all following?" -> GET /user/following
- "Get following details?" -> GET /user/following/{username}
- "Update a following?" -> PUT /user/following/{username}
- "Delete a following?" -> DELETE /user/following/{username}
- "List all gpg_keys?" -> GET /user/gpg_keys
- "Create a gpg_key?" -> POST /user/gpg_keys
- "Get gpg_key details?" -> GET /user/gpg_keys/{gpg_key_id}
- "Delete a gpg_key?" -> DELETE /user/gpg_keys/{gpg_key_id}
- "List all installations?" -> GET /user/installations
- "List all repositories?" -> GET /user/installations/{installation_id}/repositories
- "Update a repository?" -> PUT /user/installations/{installation_id}/repositories/{repository_id}
- "Delete a repository?" -> DELETE /user/installations/{installation_id}/repositories/{repository_id}
- "List all issues?" -> GET /user/issues
- "List all keys?" -> GET /user/keys
- "Create a key?" -> POST /user/keys
- "Get key details?" -> GET /user/keys/{key_id}
- "Delete a key?" -> DELETE /user/keys/{key_id}
- "List all orgs?" -> GET /user/memberships/orgs
- "Get org details?" -> GET /user/memberships/orgs/{org}
- "Partially update a org?" -> PATCH /user/memberships/orgs/{org}
- "List all orgs?" -> GET /user/orgs
- "Create a project?" -> POST /user/projects
- "List all public_emails?" -> GET /user/public_emails
- "List all repos?" -> GET /user/repos
- "Create a repo?" -> POST /user/repos
- "List all repository_invitations?" -> GET /user/repository_invitations
- "Partially update a repository_invitation?" -> PATCH /user/repository_invitations/{invitation_id}
- "Delete a repository_invitation?" -> DELETE /user/repository_invitations/{invitation_id}
- "List all starred?" -> GET /user/starred
- "Get starred details?" -> GET /user/starred/{owner}/{repo}
- "Update a starred?" -> PUT /user/starred/{owner}/{repo}
- "Delete a starred?" -> DELETE /user/starred/{owner}/{repo}
- "List all subscriptions?" -> GET /user/subscriptions
- "List all teams?" -> GET /user/teams
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{username}
- "List all events?" -> GET /users/{username}/events
- "Get org details?" -> GET /users/{username}/events/orgs/{org}
- "List all public?" -> GET /users/{username}/events/public
- "List all followers?" -> GET /users/{username}/followers
- "List all following?" -> GET /users/{username}/following
- "Get following details?" -> GET /users/{username}/following/{target_user}
- "List all gists?" -> GET /users/{username}/gists
- "List all gpg_keys?" -> GET /users/{username}/gpg_keys
- "List all hovercard?" -> GET /users/{username}/hovercard
- "List all installation?" -> GET /users/{username}/installation
- "List all keys?" -> GET /users/{username}/keys
- "List all orgs?" -> GET /users/{username}/orgs
- "List all projects?" -> GET /users/{username}/projects
- "List all received_events?" -> GET /users/{username}/received_events
- "List all public?" -> GET /users/{username}/received_events/public
- "List all repos?" -> GET /users/{username}/repos
- "List all starred?" -> GET /users/{username}/starred
- "List all subscriptions?" -> GET /users/{username}/subscriptions
- "List all zen?" -> GET /zen

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
