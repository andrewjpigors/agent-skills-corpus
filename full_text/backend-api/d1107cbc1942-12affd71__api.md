---
name: api
description: " API skill. Use when working with  for api. Covers 327 endpoints."
version: 1.0.0
generator: lapsh
---

# 
API version: v4 - Hunt Valley

## Auth
OAuth2

## Base URL
https://app.drchrono.com

## Setup
1. Configure auth: OAuth2
2. GET /api/day_sheet_charges -- verify access
3. POST /api/claim_billing_notes -- create first claim_billing_notes

## Endpoints

327 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/day_sheet_charges | Retrieve daysheet charges report for a given date range |
| POST | /api/claim_billing_notes | Create a new billing note |
| GET | /api/claim_billing_notes | Retrieve or search billing notes |
| POST | /api/signed_consent_forms | signed_consent_forms Create |
| PATCH | /api/signed_consent_forms | signed_consent_forms Update |
| GET | /api/signed_consent_forms | signed_consent_forms Get |
| POST | /api/custom_appointment_fields | Create custom appointment fields |
| GET | /api/custom_appointment_fields | Retrieve or search custom appointment fields |
| PUT | /api/lab_orders/{id} | Update an existing lab order |
| PATCH | /api/lab_orders/{id} | Update an existing lab order |
| GET | /api/lab_orders/{id} | Retrieve an existing lab order |
| DELETE | /api/lab_orders/{id} | Delete an existing lab order |
| POST | /api/clinical_notes_list | Create clinical note list request.  Use the UUID returned in the response to retrieve the batch of records. Results returned in order of ID. |
| GET | /api/clinical_notes_list | Retrieve or search clinical notes in batches. Results returned in order of ID. |
| GET | /api/custom_vitals/{id} | Retrieve an existing custom vital type |
| PUT | /api/sublabs/{id} | Update an existing sub vendor |
| PATCH | /api/sublabs/{id} | Update an existing sub vendor |
| GET | /api/sublabs/{id} | Retrieve an existing sub vendor |
| DELETE | /api/sublabs/{id} | Delete an existing sub vendor |
| GET | /api/patients/{id}/qrda1 | Retrieve patient QRDA1 |
| POST | /api/problems | Create patient problems |
| GET | /api/problems | Retrieve or search patient problems |
| GET | /api/staff |  |
| PUT | /api/patient_messages/{id} |  |
| PATCH | /api/patient_messages/{id} |  |
| GET | /api/patient_messages/{id} |  |
| POST | /api/yellow_notepad | Create or update yellow notepad content for a specific appointment and template combination. |
| GET | /api/yellow_notepad | Retrieve yellow notepad content for a specific appointment and template combination. |
| GET | /api/eligibility_checks | Retrieve or search past eligibility checks for patient |
| PUT | /api/doctor_work_schedule/{id} | Update an existing doctor's entire work schedule |
| PATCH | /api/doctor_work_schedule/{id} | Update an existing doctor's work schedule |
| GET | /api/doctor_work_schedule/{id} | Retrieve a work schedule for the doctor (beta) |
| POST | /api/medications | Create patient medications |
| GET | /api/medications | Retrieve or search patient medications |
| POST | /api/custom_demographics | Create custom demographics fields |
| GET | /api/custom_demographics | Retrieve or search custom demographics fields |
| POST | /api/appointments_list |  |
| GET | /api/appointments_list |  |
| POST | /api/appointment_profiles | Create appointment profiles for a doctor's calendar |
| GET | /api/appointment_profiles | Retrieve or search appointment profiles for a doctor's calendar |
| POST | /api/patient_communications | Create patient communication for CQM |
| GET | /api/patient_communications | Retrieve or search patient communications for CQM |
| GET | /api/patient_authorizations | Retrieve or search patient authorizations |
| PUT | /api/appointment_profiles/{id} | Update an existing appointment profile |
| PATCH | /api/appointment_profiles/{id} | Update an existing appointment profile |
| GET | /api/appointment_profiles/{id} | Retrieve an existing appointment profile |
| DELETE | /api/appointment_profiles/{id} | Delete an existing appointment profile |
| POST | /api/messages | Create messages in doctor's message center |
| GET | /api/messages | Retrieve or search messages in doctor's message center |
| PUT | /api/clinical_note_field_values/{id} | Update an existing clinical note field value |
| PATCH | /api/clinical_note_field_values/{id} | Update an existing clinical note field value |
| GET | /api/clinical_note_field_values/{id} | Retrieve an existing clinical note field value |
| POST | /api/task_categories | Create a task category |
| GET | /api/task_categories | Retrieve or search task categories |
| GET | /api/fee_schedules_v2 |  |
| GET | /api/custom_insurance_plan_names/{id} | Retrieve an existing custom insurance plan name |
| GET | /api/care_team_members |  |
| GET | /api/user_groups | Retrieve or search user groups |
| POST | /api/line_items_list | Create a billing line items list request |
| GET | /api/line_items_list | Retrieve the list of billing line items |
| POST | /api/consent_forms/{id}/unapply_from_appointment | Unassign (unapply) a consent form from appointment |
| POST | /api/consent_forms/{id}/apply_to_appointment | Assign (apply) a consent form to appointment |
| POST | /api/consent_forms | Create a patient consent form |
| GET | /api/consent_forms | Retrieve or search patient consent forms |
| PUT | /api/reminder_profiles/{id} | Update an existing reminder profile |
| PATCH | /api/reminder_profiles/{id} | Update an existing reminder profile |
| GET | /api/reminder_profiles/{id} | Retrieve an existing reminder profile |
| DELETE | /api/reminder_profiles/{id} | Delete an existing reminder profile |
| GET | /api/day_sheet_patient_payments | Retrieve daysheet cash report for a given date range |
| POST | /api/offices/{id}/add_exam_room | Add an exam room to the office |
| GET | /api/eligibility_checks/{id} | Retrieve an existing past eligibility check |
| POST | /api/patients_list | Submit patient list request.  Use the UUID returned in the response to retrieve the batch of patients. |
| GET | /api/patients_list | Retrieve or search patients in batches. This resource returns identical data to `GET /api/patients` but uses an asynchronous batch-based approach to data delivery. This is an efficient choice for large historical record loading use cases. Retrieve the results/status of a previously created patient_list request using the UUID returned in the response. Results are ordered by patient ID number. |
| POST | /api/patient_interventions | Create patient intervention for CQM |
| GET | /api/patient_interventions | Retrieve or search patient interventions for CQM |
| POST | /api/patient_messages |  |
| GET | /api/patient_messages |  |
| PUT | /api/patient_physical_exams/{id} | Update an existing patient physical exam for CQM |
| PATCH | /api/patient_physical_exams/{id} | Update an existing patient physical exam for CQM |
| GET | /api/patient_physical_exams/{id} | Retrieve an existing patient physical exam for CQM |
| POST | /api/clinical_note_field_values | Create clinical note field value |
| GET | /api/clinical_note_field_values | Retrieve or search clinical note field values |
| GET | /api/inventory_vaccines/{id} | Retrieve an existing vaccine inventory |
| POST | /api/patients | Create patient |
| GET | /api/patients | Retrieve or search patients |
| GET | /api/implantable_devices/{id} | Retrieve an existing implantable device |
| PUT | /api/patient_communications/{id} | Update an existing patient communication for CQM |
| PATCH | /api/patient_communications/{id} | Update an existing patient communication for CQM |
| GET | /api/patient_communications/{id} | Retrieve an existing patient communication for CQM |
| GET | /api/offices | Retrieve or search offices |
| GET | /api/prescription_messages/{id} | Retrieve an existing prescription message |
| GET | /api/implantable_devices | Retrieve or search implantable devices |
| POST | /api/patient_risk_assessments |  |
| GET | /api/patient_risk_assessments |  |
| PUT | /api/task_statuses/{id} | Update an existing task status |
| PATCH | /api/task_statuses/{id} | Update an existing task status |
| GET | /api/task_statuses/{id} | Retrieve an existing task status |
| POST | /api/patients_summary |  |
| GET | /api/patients_summary |  |
| PUT | /api/documents/{id} | Update an existing appointment template |
| PATCH | /api/documents/{id} | Update an existing appointment template |
| GET | /api/documents/{id} | Retrieve an existing appointment template |
| DELETE | /api/documents/{id} | Delete an existing appointment template |
| GET | /api/office_work_schedule | Get the work schedule for the authed doctor's primary office (beta) |
| POST | /api/patients/{id}/onpatient_access | Send new onpatient invite to patient |
| GET | /api/patients/{id}/onpatient_access | Retrieve or search existing onpatient access invites |
| DELETE | /api/patients/{id}/onpatient_access | Revoke sent onpatient invites |
| POST | /api/comm_logs | Create communication (phone call) logs |
| GET | /api/comm_logs | Retrieve or search communicatioin (phone call) logs |
| PUT | /api/lab_results/{id} | Update an existing lab result |
| PATCH | /api/lab_results/{id} | Update an existing lab result |
| GET | /api/lab_results/{id} | Retrieve an existing lab result |
| DELETE | /api/lab_results/{id} | Delete an existing lab result |
| PUT | /api/medications/{id} | Update an existing patient medications |
| PATCH | /api/medications/{id} | Update an existing patient medications |
| GET | /api/medications/{id} | Retrieve an existing patient medications |
| GET | /api/day_sheet_credits | Retrieve daysheet credits/adjustments report for a given date range |
| POST | /api/task_templates | Create a task template |
| GET | /api/task_templates | Retrieve or search task templates |
| POST | /api/transactions_list | Create transactions list request.  Use the UUID returned in the response to retrieve the batch of records. Results returned in order of id or updated_at. |
| GET | /api/transactions_list | Retrieve or search transactions in batches. Results returned in order of ID or updated_at. |
| PATCH | /api/medications/{id}/append_to_pharmacy_note | Append a message to the "pharmacy_note" section of the prescription, in a new paragraph |
| PUT | /api/office_work_schedule/{id} | Update an existing office's entire work schedule |
| PATCH | /api/office_work_schedule/{id} | Update an existing office's work schedule |
| GET | /api/office_work_schedule/{id} | Retrieve a work schedule (beta) |
| PUT | /api/patient_vaccine_records/{id} | Update an existing patient vaccine records |
| PATCH | /api/patient_vaccine_records/{id} | Update an existing patient vaccine records |
| GET | /api/patient_vaccine_records/{id} | Retrieve an existing patient vaccine records |
| PUT | /api/patient_flag_types/{id} | Update an existing patient flag type |
| PATCH | /api/patient_flag_types/{id} | Update an existing patient flag type |
| GET | /api/patient_flag_types/{id} | Retrieve an existing patient flag type |
| GET | /api/inventory_categories/{id} | Retrieve an existing inventory category |
| PATCH | /api/clinical_note_field_types/{id} | Update the `freedraw_image_size` of an existing clinical note FreeDraw Field |
| GET | /api/clinical_note_field_types/{id} | Retrieve an existing clinial note field type |
| PUT | /api/tasks/{id} | Update an existing task |
| PATCH | /api/tasks/{id} | Update an existing task |
| GET | /api/tasks/{id} | Retrieve an existing task |
| GET | /api/doctor_work_schedule | Get the work schedule for the authed doctor's primary office (beta) |
| GET | /api/doctor_options | Retrieve or search doctor options within practice group |
| GET | /api/fee_schedules |  |
| PUT | /api/patient_risk_assessments/{id} |  |
| PATCH | /api/patient_risk_assessments/{id} |  |
| GET | /api/patient_risk_assessments/{id} |  |
| GET | /api/inventory_categories | Retrieve or search inventory categories |
| PUT | /api/lab_documents/{id} | Update an existing lab order document |
| PATCH | /api/lab_documents/{id} | Update an existing lab order document |
| GET | /api/lab_documents/{id} | Retrieve an existing lab order document |
| DELETE | /api/lab_documents/{id} | Delete an existing lab order document |
| PUT | /api/appointment_templates/{id} | Update an existing appointment template |
| PATCH | /api/appointment_templates/{id} | Update an existing appointment template |
| GET | /api/appointment_templates/{id} | Retrieve an existing appointment template |
| DELETE | /api/appointment_templates/{id} | Delete an existing appointment template |
| PUT | /api/patient_interventions/{id} | Update an existing patient intervention for CQM |
| PATCH | /api/patient_interventions/{id} | Update an existing patient intervention for CQM |
| GET | /api/patient_interventions/{id} | Retrieve an existing patient intervention for CQM |
| POST | /api/task_statuses | Create a task status |
| GET | /api/task_statuses | Retrieve or search task statuses |
| PUT | /api/allergies/{id} | Update an existing patient allergy |
| PATCH | /api/allergies/{id} | Update an existing patient allergy |
| GET | /api/allergies/{id} | Retrieve an existing patient allergy |
| GET | /api/patients/{id}/ccda | Retrieve patient CCDA |
| GET | /api/patient_payments/{id} | Retrieve an existing patient payment |
| GET | /api/lab_orders_summary |  |
| POST | /api/patient_payments | Create patient payment |
| GET | /api/patient_payments | Retrieve or search patient payments |
| POST | /api/clinical_note_field_values_list | Create clinical note field value list request.  Use the UUID returned in the response to retrieve the batch of records. Results returned in order of ID. |
| GET | /api/clinical_note_field_values_list | Retrieve or search clinical note values (soap notes) in batches. Results returned in order of ID or by updated_at. |
| GET | /api/care_plans/{id} | Retrieve an existing care plan |
| GET | /api/billing_profiles | Retrieve or search billing profiles |
| GET | /api/billing_profiles/{id} | Retrieve an existing billing profiles |
| GET | /api/availability | Retrieve availability slots for the given date and office, doctor, or exam room. |
| PUT | /api/task_templates/{id} | Update an existing task template |
| PATCH | /api/task_templates/{id} | Update an existing task template |
| GET | /api/task_templates/{id} | Retrieve an existing task template |
| GET | /api/fee_schedules/{id} |  |
| PUT | /api/appointments/{id} | Update an existing appointment or break |
| PATCH | /api/appointments/{id} | Update an existing appointment or break |
| GET | /api/appointments/{id} | Retrieve an existing appointment or break |
| DELETE | /api/appointments/{id} | Delete an existing appointment or break |
| POST | /api/telehealth_appointments |  |
| GET | /api/telehealth_appointments |  |
| GET | /api/care_plans | Retrieve or search care plans |
| POST | /api/patient_physical_exams | Create patient physical exam for CQM |
| GET | /api/patient_physical_exams | Retrieve or search patient physical exams for CQM |
| GET | /api/line_item_deletions | Retrieve or search billing line item deletions. When a billing line item is deleted, a record of its original ID and the appointment it was attached to will be logged and is accessible from this resource. |
| GET | /api/signed_consent_forms/{id} | signed_consent_forms Read |
| GET | /api/clinical_note_templates/{id} | Retrieve an existing clinical note tempalte |
| GET | /api/transactions | Retrieve or search insurance transactions associated with billing line items |
| POST | /api/lab_results | Create lab results. An example lab workflow is as following: |
| GET | /api/lab_results | Retrieve or search lab results |
| GET | /api/custom_insurance_plan_names | Retrieve or search custom insurance plan names |
| PUT | /api/problems/{id} | Update an existing patient problems |
| PATCH | /api/problems/{id} | Update an existing patient problems |
| GET | /api/problems/{id} | Retrieve an existing patient problems |
| POST | /api/amendments | Create patient amendments to a patient's clinical records |
| GET | /api/amendments | Retrieve or search patient amendments. You can only interact with amendments created by your API application |
| POST | /api/lab_orders | Create lab orders. An example lab workflow is as following: |
| GET | /api/lab_orders | Retrieve or search lab orders |
| GET | /api/doctors/{id} | Retrieve an existing doctor |
| POST | /api/patient_flag_types | Create patient flag types |
| GET | /api/patient_flag_types | Retrieve or search patient flag types |
| GET | /api/day_sheet_totals | Retrieve daysheet totals report for a given date range |
| PUT | /api/custom_appointment_fields/{id} | Update an existing custom appointment field |
| PATCH | /api/custom_appointment_fields/{id} | Update an existing custom appointment field |
| GET | /api/custom_appointment_fields/{id} | Retrieve an existing custom appointment field |
| POST | /api/eobs | Create EOB object |
| GET | /api/eobs | Retrieve or search EOB objects |
| GET | /api/users/{id} | Retrieve an existing user, `/api/users/current` can be used to identify logged in user, it will redirect to `/api/users/{current_user_id}` |
| GET | /api/insurances |  |
| POST | /api/telehealth_appointment_history |  |
| GET | /api/telehealth_appointment_history |  |
| POST | /api/task_notes | Create a task note |
| GET | /api/task_notes | Retrieve or search task notes |
| POST | /api/tasks | Create a task |
| GET | /api/tasks | Retrieve or search tasks |
| PUT | /api/patients_summary/{id} |  |
| PATCH | /api/patients_summary/{id} |  |
| GET | /api/patients_summary/{id} |  |
| DELETE | /api/patients_summary/{id} |  |
| POST | /api/lab_documents | Create lab order documents. An example lab workflow is as following: |
| GET | /api/lab_documents | Retrieve or search lab order documents |
| PUT | /api/consent_forms/{id} | Update an existing patient consent form |
| PATCH | /api/consent_forms/{id} | Update an existing patient consent form |
| GET | /api/consent_forms/{id} | Retrieve an existing patient consent form |
| PUT | /api/lab_tests/{id} | Update an existing lab test |
| PATCH | /api/lab_tests/{id} | Update an existing lab test |
| GET | /api/lab_tests/{id} | Retrieve an existing lab test |
| DELETE | /api/lab_tests/{id} | Delete an existing lab test |
| POST | /api/prescription_messages_list | Create prescription messages list request.  Use the UUID returned in the response to retrieve the batch of records. Results returned in order of id or updated_at. |
| GET | /api/prescription_messages_list | Retrieve or search prescription messages in batches. Results returned in order of ID or updated_at. |
| PUT | /api/patients/{id} | Update an existing patient |
| PATCH | /api/patients/{id} | Update an existing patient |
| GET | /api/patients/{id} | Retrieve an existing patient |
| DELETE | /api/patients/{id} | Delete an existing patient |
| GET | /api/patients/{id}/ccda_async | Retrieve patient CCDA async. |
| GET | /api/custom_vitals | Retrieve or search custom vital types |
| POST | /api/schedule_blocks | Create a schedule block |
| GET | /api/schedule_blocks | Retrieve and search schedule blocks |
| GET | /api/care_team_members/{id} |  |
| GET | /api/claim_billing_notes/{id} | Retrieve an existing billing note |
| POST | /api/inventory_vaccines | Create vaccine inventory |
| GET | /api/inventory_vaccines | Retrieve or search vaccine inventories |
| GET | /api/transactions/{id} | Retrieve an existing insurance transaction |
| GET | /api/procedures |  |
| PUT | /api/patient_lab_results/{id} |  |
| PATCH | /api/patient_lab_results/{id} |  |
| GET | /api/patient_lab_results/{id} |  |
| DELETE | /api/patient_lab_results/{id} |  |
| PUT | /api/amendments/{id} | Update an existing patient amendment, you can only interact with amendments created by your API application |
| PATCH | /api/amendments/{id} | Update an existing patient amendment, you can only interact with amendments created by your API application |
| GET | /api/amendments/{id} | Retrieve an existing patient amendment, you can only interact with amendments created by your API application |
| DELETE | /api/amendments/{id} | Delete an existing patient amendment, you can only interact with amendments created by your API application |
| POST | /api/lab_tests | Create lab tests. An example lab workflow is as following: |
| GET | /api/lab_tests | Retrieve or search lab tests |
| PUT | /api/appointments_list/{id} |  |
| PATCH | /api/appointments_list/{id} |  |
| GET | /api/appointments_list/{id} |  |
| DELETE | /api/appointments_list/{id} |  |
| POST | /api/patient_lab_results |  |
| GET | /api/patient_lab_results |  |
| PUT | /api/task_categories/{id} | Update an existing task category |
| PATCH | /api/task_categories/{id} | Update an existing task category |
| GET | /api/task_categories/{id} | Retrieve an existing task category |
| GET | /api/fee_schedules_v2/{id} |  |
| GET | /api/insurances/{id} |  |
| GET | /api/clinical_notes |  |
| POST | /api/eligibility_checks_list | Create eligibility checks list request.  Use the UUID returned in the response to retrieve the batch of records. Results returned in order of id or updated_at. |
| GET | /api/eligibility_checks_list | Retrieve or search eligibility checks in batches. Results returned in order of ID or updated_at. |
| GET | /api/telehealth_appointment_history/{id} |  |
| GET | /api/clinical_notes/{id} |  |
| GET | /api/clinical_note_field_types | Retrieve or search clinical note field types |
| POST | /api/documents | Create documents |
| GET | /api/documents | Retrieve or search documents |
| GET | /api/staff/{id} |  |
| GET | /api/users | Retrieve or search users, `/api/users/current` can be used to identify logged in user, it will redirect to `/api/users/{current_user_id}` |
| PUT | /api/schedule_blocks/{id} | Update a schedule block |
| PATCH | /api/schedule_blocks/{id} | Partially update a schedule block |
| GET | /api/schedule_blocks/{id} | Retrieve a schedule block |
| DELETE | /api/schedule_blocks/{id} | Delete a schedule block |
| GET | /api/lab_orders_summary/{id} |  |
| GET | /api/audit_log | Retrieve or search audit logs. |
| PUT | /api/task_notes/{id} | Update an existing task note |
| PATCH | /api/task_notes/{id} | Update an existing task note |
| GET | /api/task_notes/{id} | Retrieve an existing task note |
| PUT | /api/custom_demographics/{id} | Update an existing custom demographics field |
| PATCH | /api/custom_demographics/{id} | Update an existing custom demographics field |
| GET | /api/custom_demographics/{id} | Retrieve an existing custom demographics field |
| PUT | /api/messages/{id} | Update an existing message in doctor's message center |
| PATCH | /api/messages/{id} | Update an existing message in doctor's message center |
| GET | /api/messages/{id} | Retrieve an existing message in doctor's message center |
| DELETE | /api/messages/{id} | Delete an existing message in doctor's message center |
| GET | /api/eobs/{id} | Retrieve an existing EOB object |
| GET | /api/doctor_options/{id} | Retrieve existing options for a doctor |
| POST | /api/allergies | Create patient allergy |
| GET | /api/allergies | Retrieve or search patient allergies |
| POST | /api/appointments | Create a new appointment or break on doctor's calendar |
| GET | /api/appointments | Retrieve or search appointment or breaks. |
| GET | /api/procedures/{id} |  |
| GET | /api/clinical_note_templates | Retrieve or search clinical note templates |
| PUT | /api/line_items/{id} |  |
| PATCH | /api/line_items/{id} |  |
| GET | /api/line_items/{id} | Retrieve an existing billing line item |
| DELETE | /api/line_items/{id} |  |
| GET | /api/doctors | Retrieve or search doctors within practice group |
| POST | /api/reminder_profiles | Create reminder profile |
| GET | /api/reminder_profiles | Retrieve or search reminder profiles |
| GET | /api/patient_payment_log | Retrieve or search patient payment logs |
| PUT | /api/offices/{id} | Update an existing office |
| PATCH | /api/offices/{id} | Update an existing office |
| GET | /api/offices/{id} | Retrieve an existing office |
| GET | /api/patient_payment_log/{id} | Retrieve an existing patient payment log |
| POST | /api/appointment_templates | Create appointment templates for a doctor's calendar |
| GET | /api/appointment_templates | Retrieve or search appointment templates for a doctor's calendar |
| POST | /api/patient_vaccine_records | Create patient vaccine records |
| GET | /api/patient_vaccine_records | Retrieve or search patient vaccine records |
| PUT | /api/telehealth_appointments/{id} |  |
| PATCH | /api/telehealth_appointments/{id} |  |
| GET | /api/telehealth_appointments/{id} |  |
| PUT | /api/comm_logs/{id} | Update an existing communication (phone call) logs |
| PATCH | /api/comm_logs/{id} | Update an existing communication (phone call) logs |
| GET | /api/comm_logs/{id} | Retrieve an existing communication (phone call) logs |
| GET | /api/prescription_messages | Retrieve or search prescription messages |
| GET | /api/user_groups/{id} | Retrieve an existing user group |
| POST | /api/line_items | Create billing line item for appointments |
| GET | /api/line_items | Retrieve or search billing line items |
| POST | /api/sublabs | Create sub-vendors |
| GET | /api/sublabs | Retrieve or search sub vendors |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all day_sheet_charges?" -> GET /api/day_sheet_charges
- "Create a claim_billing_note?" -> POST /api/claim_billing_notes
- "List all claim_billing_notes?" -> GET /api/claim_billing_notes
- "Create a signed_consent_form?" -> POST /api/signed_consent_forms
- "List all signed_consent_forms?" -> GET /api/signed_consent_forms
- "Create a custom_appointment_field?" -> POST /api/custom_appointment_fields
- "List all custom_appointment_fields?" -> GET /api/custom_appointment_fields
- "Update a lab_order?" -> PUT /api/lab_orders/{id}
- "Partially update a lab_order?" -> PATCH /api/lab_orders/{id}
- "Get lab_order details?" -> GET /api/lab_orders/{id}
- "Delete a lab_order?" -> DELETE /api/lab_orders/{id}
- "Create a clinical_notes_list?" -> POST /api/clinical_notes_list
- "List all clinical_notes_list?" -> GET /api/clinical_notes_list
- "Get custom_vital details?" -> GET /api/custom_vitals/{id}
- "Update a sublab?" -> PUT /api/sublabs/{id}
- "Partially update a sublab?" -> PATCH /api/sublabs/{id}
- "Get sublab details?" -> GET /api/sublabs/{id}
- "Delete a sublab?" -> DELETE /api/sublabs/{id}
- "List all qrda1?" -> GET /api/patients/{id}/qrda1
- "Create a problem?" -> POST /api/problems
- "List all problems?" -> GET /api/problems
- "List all staff?" -> GET /api/staff
- "Update a patient_message?" -> PUT /api/patient_messages/{id}
- "Partially update a patient_message?" -> PATCH /api/patient_messages/{id}
- "Get patient_message details?" -> GET /api/patient_messages/{id}
- "Create a yellow_notepad?" -> POST /api/yellow_notepad
- "List all yellow_notepad?" -> GET /api/yellow_notepad
- "List all eligibility_checks?" -> GET /api/eligibility_checks
- "Update a doctor_work_schedule?" -> PUT /api/doctor_work_schedule/{id}
- "Partially update a doctor_work_schedule?" -> PATCH /api/doctor_work_schedule/{id}
- "Get doctor_work_schedule details?" -> GET /api/doctor_work_schedule/{id}
- "Create a medication?" -> POST /api/medications
- "List all medications?" -> GET /api/medications
- "Create a custom_demographic?" -> POST /api/custom_demographics
- "List all custom_demographics?" -> GET /api/custom_demographics
- "Create a appointments_list?" -> POST /api/appointments_list
- "List all appointments_list?" -> GET /api/appointments_list
- "Create a appointment_profile?" -> POST /api/appointment_profiles
- "List all appointment_profiles?" -> GET /api/appointment_profiles
- "Create a patient_communication?" -> POST /api/patient_communications
- "List all patient_communications?" -> GET /api/patient_communications
- "List all patient_authorizations?" -> GET /api/patient_authorizations
- "Update a appointment_profile?" -> PUT /api/appointment_profiles/{id}
- "Partially update a appointment_profile?" -> PATCH /api/appointment_profiles/{id}
- "Get appointment_profile details?" -> GET /api/appointment_profiles/{id}
- "Delete a appointment_profile?" -> DELETE /api/appointment_profiles/{id}
- "Create a message?" -> POST /api/messages
- "List all messages?" -> GET /api/messages
- "Update a clinical_note_field_value?" -> PUT /api/clinical_note_field_values/{id}
- "Partially update a clinical_note_field_value?" -> PATCH /api/clinical_note_field_values/{id}
- "Get clinical_note_field_value details?" -> GET /api/clinical_note_field_values/{id}
- "Create a task_category?" -> POST /api/task_categories
- "List all task_categories?" -> GET /api/task_categories
- "List all fee_schedules_v2?" -> GET /api/fee_schedules_v2
- "Get custom_insurance_plan_name details?" -> GET /api/custom_insurance_plan_names/{id}
- "List all care_team_members?" -> GET /api/care_team_members
- "List all user_groups?" -> GET /api/user_groups
- "Create a line_items_list?" -> POST /api/line_items_list
- "List all line_items_list?" -> GET /api/line_items_list
- "Create a unapply_from_appointment?" -> POST /api/consent_forms/{id}/unapply_from_appointment
- "Create a apply_to_appointment?" -> POST /api/consent_forms/{id}/apply_to_appointment
- "Create a consent_form?" -> POST /api/consent_forms
- "List all consent_forms?" -> GET /api/consent_forms
- "Update a reminder_profile?" -> PUT /api/reminder_profiles/{id}
- "Partially update a reminder_profile?" -> PATCH /api/reminder_profiles/{id}
- "Get reminder_profile details?" -> GET /api/reminder_profiles/{id}
- "Delete a reminder_profile?" -> DELETE /api/reminder_profiles/{id}
- "List all day_sheet_patient_payments?" -> GET /api/day_sheet_patient_payments
- "Create a add_exam_room?" -> POST /api/offices/{id}/add_exam_room
- "Get eligibility_check details?" -> GET /api/eligibility_checks/{id}
- "Create a patients_list?" -> POST /api/patients_list
- "List all patients_list?" -> GET /api/patients_list
- "Create a patient_intervention?" -> POST /api/patient_interventions
- "List all patient_interventions?" -> GET /api/patient_interventions
- "Create a patient_message?" -> POST /api/patient_messages
- "List all patient_messages?" -> GET /api/patient_messages
- "Update a patient_physical_exam?" -> PUT /api/patient_physical_exams/{id}
- "Partially update a patient_physical_exam?" -> PATCH /api/patient_physical_exams/{id}
- "Get patient_physical_exam details?" -> GET /api/patient_physical_exams/{id}
- "Create a clinical_note_field_value?" -> POST /api/clinical_note_field_values
- "List all clinical_note_field_values?" -> GET /api/clinical_note_field_values
- "Get inventory_vaccine details?" -> GET /api/inventory_vaccines/{id}
- "Create a patient?" -> POST /api/patients
- "List all patients?" -> GET /api/patients
- "Get implantable_device details?" -> GET /api/implantable_devices/{id}
- "Update a patient_communication?" -> PUT /api/patient_communications/{id}
- "Partially update a patient_communication?" -> PATCH /api/patient_communications/{id}
- "Get patient_communication details?" -> GET /api/patient_communications/{id}
- "List all offices?" -> GET /api/offices
- "Get prescription_message details?" -> GET /api/prescription_messages/{id}
- "List all implantable_devices?" -> GET /api/implantable_devices
- "Create a patient_risk_assessment?" -> POST /api/patient_risk_assessments
- "List all patient_risk_assessments?" -> GET /api/patient_risk_assessments
- "Update a task_statuse?" -> PUT /api/task_statuses/{id}
- "Partially update a task_statuse?" -> PATCH /api/task_statuses/{id}
- "Get task_statuse details?" -> GET /api/task_statuses/{id}
- "Create a patients_summary?" -> POST /api/patients_summary
- "List all patients_summary?" -> GET /api/patients_summary
- "Update a document?" -> PUT /api/documents/{id}
- "Partially update a document?" -> PATCH /api/documents/{id}
- "Get document details?" -> GET /api/documents/{id}
- "Delete a document?" -> DELETE /api/documents/{id}
- "List all office_work_schedule?" -> GET /api/office_work_schedule
- "Create a onpatient_access?" -> POST /api/patients/{id}/onpatient_access
- "List all onpatient_access?" -> GET /api/patients/{id}/onpatient_access
- "Create a comm_log?" -> POST /api/comm_logs
- "List all comm_logs?" -> GET /api/comm_logs
- "Update a lab_result?" -> PUT /api/lab_results/{id}
- "Partially update a lab_result?" -> PATCH /api/lab_results/{id}
- "Get lab_result details?" -> GET /api/lab_results/{id}
- "Delete a lab_result?" -> DELETE /api/lab_results/{id}
- "Update a medication?" -> PUT /api/medications/{id}
- "Partially update a medication?" -> PATCH /api/medications/{id}
- "Get medication details?" -> GET /api/medications/{id}
- "List all day_sheet_credits?" -> GET /api/day_sheet_credits
- "Create a task_template?" -> POST /api/task_templates
- "List all task_templates?" -> GET /api/task_templates
- "Create a transactions_list?" -> POST /api/transactions_list
- "List all transactions_list?" -> GET /api/transactions_list
- "Update a office_work_schedule?" -> PUT /api/office_work_schedule/{id}
- "Partially update a office_work_schedule?" -> PATCH /api/office_work_schedule/{id}
- "Get office_work_schedule details?" -> GET /api/office_work_schedule/{id}
- "Update a patient_vaccine_record?" -> PUT /api/patient_vaccine_records/{id}
- "Partially update a patient_vaccine_record?" -> PATCH /api/patient_vaccine_records/{id}
- "Get patient_vaccine_record details?" -> GET /api/patient_vaccine_records/{id}
- "Update a patient_flag_type?" -> PUT /api/patient_flag_types/{id}
- "Partially update a patient_flag_type?" -> PATCH /api/patient_flag_types/{id}
- "Get patient_flag_type details?" -> GET /api/patient_flag_types/{id}
- "Get inventory_category details?" -> GET /api/inventory_categories/{id}
- "Partially update a clinical_note_field_type?" -> PATCH /api/clinical_note_field_types/{id}
- "Get clinical_note_field_type details?" -> GET /api/clinical_note_field_types/{id}
- "Update a task?" -> PUT /api/tasks/{id}
- "Partially update a task?" -> PATCH /api/tasks/{id}
- "Get task details?" -> GET /api/tasks/{id}
- "List all doctor_work_schedule?" -> GET /api/doctor_work_schedule
- "List all doctor_options?" -> GET /api/doctor_options
- "List all fee_schedules?" -> GET /api/fee_schedules
- "Update a patient_risk_assessment?" -> PUT /api/patient_risk_assessments/{id}
- "Partially update a patient_risk_assessment?" -> PATCH /api/patient_risk_assessments/{id}
- "Get patient_risk_assessment details?" -> GET /api/patient_risk_assessments/{id}
- "List all inventory_categories?" -> GET /api/inventory_categories
- "Update a lab_document?" -> PUT /api/lab_documents/{id}
- "Partially update a lab_document?" -> PATCH /api/lab_documents/{id}
- "Get lab_document details?" -> GET /api/lab_documents/{id}
- "Delete a lab_document?" -> DELETE /api/lab_documents/{id}
- "Update a appointment_template?" -> PUT /api/appointment_templates/{id}
- "Partially update a appointment_template?" -> PATCH /api/appointment_templates/{id}
- "Get appointment_template details?" -> GET /api/appointment_templates/{id}
- "Delete a appointment_template?" -> DELETE /api/appointment_templates/{id}
- "Update a patient_intervention?" -> PUT /api/patient_interventions/{id}
- "Partially update a patient_intervention?" -> PATCH /api/patient_interventions/{id}
- "Get patient_intervention details?" -> GET /api/patient_interventions/{id}
- "Create a task_statuse?" -> POST /api/task_statuses
- "List all task_statuses?" -> GET /api/task_statuses
- "Update a allergy?" -> PUT /api/allergies/{id}
- "Partially update a allergy?" -> PATCH /api/allergies/{id}
- "Get allergy details?" -> GET /api/allergies/{id}
- "List all ccda?" -> GET /api/patients/{id}/ccda
- "Get patient_payment details?" -> GET /api/patient_payments/{id}
- "List all lab_orders_summary?" -> GET /api/lab_orders_summary
- "Create a patient_payment?" -> POST /api/patient_payments
- "List all patient_payments?" -> GET /api/patient_payments
- "Create a clinical_note_field_values_list?" -> POST /api/clinical_note_field_values_list
- "List all clinical_note_field_values_list?" -> GET /api/clinical_note_field_values_list
- "Get care_plan details?" -> GET /api/care_plans/{id}
- "List all billing_profiles?" -> GET /api/billing_profiles
- "Get billing_profile details?" -> GET /api/billing_profiles/{id}
- "List all availability?" -> GET /api/availability
- "Update a task_template?" -> PUT /api/task_templates/{id}
- "Partially update a task_template?" -> PATCH /api/task_templates/{id}
- "Get task_template details?" -> GET /api/task_templates/{id}
- "Get fee_schedule details?" -> GET /api/fee_schedules/{id}
- "Update a appointment?" -> PUT /api/appointments/{id}
- "Partially update a appointment?" -> PATCH /api/appointments/{id}
- "Get appointment details?" -> GET /api/appointments/{id}
- "Delete a appointment?" -> DELETE /api/appointments/{id}
- "Create a telehealth_appointment?" -> POST /api/telehealth_appointments
- "List all telehealth_appointments?" -> GET /api/telehealth_appointments
- "List all care_plans?" -> GET /api/care_plans
- "Create a patient_physical_exam?" -> POST /api/patient_physical_exams
- "List all patient_physical_exams?" -> GET /api/patient_physical_exams
- "List all line_item_deletions?" -> GET /api/line_item_deletions
- "Get signed_consent_form details?" -> GET /api/signed_consent_forms/{id}
- "Get clinical_note_template details?" -> GET /api/clinical_note_templates/{id}
- "List all transactions?" -> GET /api/transactions
- "Create a lab_result?" -> POST /api/lab_results
- "List all lab_results?" -> GET /api/lab_results
- "List all custom_insurance_plan_names?" -> GET /api/custom_insurance_plan_names
- "Update a problem?" -> PUT /api/problems/{id}
- "Partially update a problem?" -> PATCH /api/problems/{id}
- "Get problem details?" -> GET /api/problems/{id}
- "Create a amendment?" -> POST /api/amendments
- "List all amendments?" -> GET /api/amendments
- "Create a lab_order?" -> POST /api/lab_orders
- "List all lab_orders?" -> GET /api/lab_orders
- "Get doctor details?" -> GET /api/doctors/{id}
- "Create a patient_flag_type?" -> POST /api/patient_flag_types
- "List all patient_flag_types?" -> GET /api/patient_flag_types
- "List all day_sheet_totals?" -> GET /api/day_sheet_totals
- "Update a custom_appointment_field?" -> PUT /api/custom_appointment_fields/{id}
- "Partially update a custom_appointment_field?" -> PATCH /api/custom_appointment_fields/{id}
- "Get custom_appointment_field details?" -> GET /api/custom_appointment_fields/{id}
- "Create a eob?" -> POST /api/eobs
- "List all eobs?" -> GET /api/eobs
- "Get user details?" -> GET /api/users/{id}
- "List all insurances?" -> GET /api/insurances
- "Create a telehealth_appointment_history?" -> POST /api/telehealth_appointment_history
- "List all telehealth_appointment_history?" -> GET /api/telehealth_appointment_history
- "Create a task_note?" -> POST /api/task_notes
- "List all task_notes?" -> GET /api/task_notes
- "Create a task?" -> POST /api/tasks
- "List all tasks?" -> GET /api/tasks
- "Update a patients_summary?" -> PUT /api/patients_summary/{id}
- "Partially update a patients_summary?" -> PATCH /api/patients_summary/{id}
- "Get patients_summary details?" -> GET /api/patients_summary/{id}
- "Delete a patients_summary?" -> DELETE /api/patients_summary/{id}
- "Create a lab_document?" -> POST /api/lab_documents
- "List all lab_documents?" -> GET /api/lab_documents
- "Update a consent_form?" -> PUT /api/consent_forms/{id}
- "Partially update a consent_form?" -> PATCH /api/consent_forms/{id}
- "Get consent_form details?" -> GET /api/consent_forms/{id}
- "Update a lab_test?" -> PUT /api/lab_tests/{id}
- "Partially update a lab_test?" -> PATCH /api/lab_tests/{id}
- "Get lab_test details?" -> GET /api/lab_tests/{id}
- "Delete a lab_test?" -> DELETE /api/lab_tests/{id}
- "Create a prescription_messages_list?" -> POST /api/prescription_messages_list
- "List all prescription_messages_list?" -> GET /api/prescription_messages_list
- "Update a patient?" -> PUT /api/patients/{id}
- "Partially update a patient?" -> PATCH /api/patients/{id}
- "Get patient details?" -> GET /api/patients/{id}
- "Delete a patient?" -> DELETE /api/patients/{id}
- "List all ccda_async?" -> GET /api/patients/{id}/ccda_async
- "List all custom_vitals?" -> GET /api/custom_vitals
- "Create a schedule_block?" -> POST /api/schedule_blocks
- "List all schedule_blocks?" -> GET /api/schedule_blocks
- "Get care_team_member details?" -> GET /api/care_team_members/{id}
- "Get claim_billing_note details?" -> GET /api/claim_billing_notes/{id}
- "Create a inventory_vaccine?" -> POST /api/inventory_vaccines
- "List all inventory_vaccines?" -> GET /api/inventory_vaccines
- "Get transaction details?" -> GET /api/transactions/{id}
- "List all procedures?" -> GET /api/procedures
- "Update a patient_lab_result?" -> PUT /api/patient_lab_results/{id}
- "Partially update a patient_lab_result?" -> PATCH /api/patient_lab_results/{id}
- "Get patient_lab_result details?" -> GET /api/patient_lab_results/{id}
- "Delete a patient_lab_result?" -> DELETE /api/patient_lab_results/{id}
- "Update a amendment?" -> PUT /api/amendments/{id}
- "Partially update a amendment?" -> PATCH /api/amendments/{id}
- "Get amendment details?" -> GET /api/amendments/{id}
- "Delete a amendment?" -> DELETE /api/amendments/{id}
- "Create a lab_test?" -> POST /api/lab_tests
- "List all lab_tests?" -> GET /api/lab_tests
- "Update a appointments_list?" -> PUT /api/appointments_list/{id}
- "Partially update a appointments_list?" -> PATCH /api/appointments_list/{id}
- "Get appointments_list details?" -> GET /api/appointments_list/{id}
- "Delete a appointments_list?" -> DELETE /api/appointments_list/{id}
- "Create a patient_lab_result?" -> POST /api/patient_lab_results
- "List all patient_lab_results?" -> GET /api/patient_lab_results
- "Update a task_category?" -> PUT /api/task_categories/{id}
- "Partially update a task_category?" -> PATCH /api/task_categories/{id}
- "Get task_category details?" -> GET /api/task_categories/{id}
- "Get fee_schedules_v2 details?" -> GET /api/fee_schedules_v2/{id}
- "Get insurance details?" -> GET /api/insurances/{id}
- "List all clinical_notes?" -> GET /api/clinical_notes
- "Create a eligibility_checks_list?" -> POST /api/eligibility_checks_list
- "List all eligibility_checks_list?" -> GET /api/eligibility_checks_list
- "Get telehealth_appointment_history details?" -> GET /api/telehealth_appointment_history/{id}
- "Get clinical_note details?" -> GET /api/clinical_notes/{id}
- "List all clinical_note_field_types?" -> GET /api/clinical_note_field_types
- "Create a document?" -> POST /api/documents
- "List all documents?" -> GET /api/documents
- "Get staff details?" -> GET /api/staff/{id}
- "List all users?" -> GET /api/users
- "Update a schedule_block?" -> PUT /api/schedule_blocks/{id}
- "Partially update a schedule_block?" -> PATCH /api/schedule_blocks/{id}
- "Get schedule_block details?" -> GET /api/schedule_blocks/{id}
- "Delete a schedule_block?" -> DELETE /api/schedule_blocks/{id}
- "Get lab_orders_summary details?" -> GET /api/lab_orders_summary/{id}
- "List all audit_log?" -> GET /api/audit_log
- "Update a task_note?" -> PUT /api/task_notes/{id}
- "Partially update a task_note?" -> PATCH /api/task_notes/{id}
- "Get task_note details?" -> GET /api/task_notes/{id}
- "Update a custom_demographic?" -> PUT /api/custom_demographics/{id}
- "Partially update a custom_demographic?" -> PATCH /api/custom_demographics/{id}
- "Get custom_demographic details?" -> GET /api/custom_demographics/{id}
- "Update a message?" -> PUT /api/messages/{id}
- "Partially update a message?" -> PATCH /api/messages/{id}
- "Get message details?" -> GET /api/messages/{id}
- "Delete a message?" -> DELETE /api/messages/{id}
- "Get eob details?" -> GET /api/eobs/{id}
- "Get doctor_option details?" -> GET /api/doctor_options/{id}
- "Create a allergy?" -> POST /api/allergies
- "List all allergies?" -> GET /api/allergies
- "Create a appointment?" -> POST /api/appointments
- "List all appointments?" -> GET /api/appointments
- "Get procedure details?" -> GET /api/procedures/{id}
- "List all clinical_note_templates?" -> GET /api/clinical_note_templates
- "Update a line_item?" -> PUT /api/line_items/{id}
- "Partially update a line_item?" -> PATCH /api/line_items/{id}
- "Get line_item details?" -> GET /api/line_items/{id}
- "Delete a line_item?" -> DELETE /api/line_items/{id}
- "List all doctors?" -> GET /api/doctors
- "Create a reminder_profile?" -> POST /api/reminder_profiles
- "List all reminder_profiles?" -> GET /api/reminder_profiles
- "List all patient_payment_log?" -> GET /api/patient_payment_log
- "Update a office?" -> PUT /api/offices/{id}
- "Partially update a office?" -> PATCH /api/offices/{id}
- "Get office details?" -> GET /api/offices/{id}
- "Get patient_payment_log details?" -> GET /api/patient_payment_log/{id}
- "Create a appointment_template?" -> POST /api/appointment_templates
- "List all appointment_templates?" -> GET /api/appointment_templates
- "Create a patient_vaccine_record?" -> POST /api/patient_vaccine_records
- "List all patient_vaccine_records?" -> GET /api/patient_vaccine_records
- "Update a telehealth_appointment?" -> PUT /api/telehealth_appointments/{id}
- "Partially update a telehealth_appointment?" -> PATCH /api/telehealth_appointments/{id}
- "Get telehealth_appointment details?" -> GET /api/telehealth_appointments/{id}
- "Update a comm_log?" -> PUT /api/comm_logs/{id}
- "Partially update a comm_log?" -> PATCH /api/comm_logs/{id}
- "Get comm_log details?" -> GET /api/comm_logs/{id}
- "List all prescription_messages?" -> GET /api/prescription_messages
- "Get user_group details?" -> GET /api/user_groups/{id}
- "Create a line_item?" -> POST /api/line_items
- "List all line_items?" -> GET /api/line_items
- "Create a sublab?" -> POST /api/sublabs
- "List all sublabs?" -> GET /api/sublabs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
