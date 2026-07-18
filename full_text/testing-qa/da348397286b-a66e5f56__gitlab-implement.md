---
name: gitlab-implement
description: Implementation guidance for the GitLab codebase — file placement, patterns, testing, and MR preparation
license: MIT
---

## Before You Start

1. Read the issue thoroughly (use issue-analyzer agent)
2. Read the relevant development guide section
3. Check if similar changes exist in the codebase (search first)

## File Placement

| What | Where |
|------|-------|
| Models | app/models/ |
| Services | app/services/ |
| Finders | app/finders/ |
| Policies | app/policies/ |
| Serializers | app/serializers/ |
| GraphQL types | app/graphql/types/ |
| GraphQL mutations | app/graphql/mutations/ |
| GraphQL resolvers | app/graphql/resolvers/ |
| Vue components | app/assets/javascripts/<feature>/components/ |
| Vue entry points | app/assets/javascripts/pages/<route>/<action>/index.js |
| Haml views | app/views/ |
| Migrations | db/migrate/ (regular) or db/post_migrate/ (post-deploy) |
| Backend specs | spec/ (mirrors app/) |
| Frontend specs | spec/frontend/ (mirrors app/assets/) |
| Docs | doc/ (mirrors docs.gitlab.com URL) |

## Ruby Patterns

- Business logic → service class (app/services/)
- Complex queries → finder (app/finders/)
- Authorization → policy (app/policies/)
- NO callbacks on ActiveRecord models
- Scopes: for_, with_, order_by_ naming

## Frontend Patterns

- Vue.js for interactive UI, mounted on Haml elements
- GraphQL for data fetching (not REST)
- Pinia for state management (not Vuex)
- Pajamas components for UI
- All strings externalized (i18n)

## Testing

- Every new class needs a spec
- Spec file mirrors app/ path exactly
- Feature-flagged code: test both on and off
- Use factories, not fixtures
- Shared examples where patterns repeat
