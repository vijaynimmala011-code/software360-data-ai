# Utilization Calculation Guide

> **Fictional training document.** All organizations, people, rules,
> thresholds, dates, costs, contacts, and examples are invented for Software
> 360. This is not an operational company policy and contains no confidential
> information.

## 1. Metric purpose

The utilization metric supports fictional license planning by comparing users
with qualifying activity to users eligible through an assignment.

## 2. Definitions

An assigned user has an active entitlement during the reporting month. An
active user has at least one qualifying, valid, deduplicated usage event in the
same month.

## 3. Calculation

Utilization percentage equals distinct active assigned users divided by
distinct assigned users, multiplied by 100. A zero denominator produces no
rate and is reported for review.

## 4. Fictional worked example

If 80 distinct users are assigned and 60 have qualifying activity, utilization
is 75 percent. The example is invented and is not a business target.

## 5. Data-quality treatment

Duplicate event identifiers are deduplicated. Null software identifiers and
negative session durations are quarantined. Raw product-name variations are
standardized against the product dimension.

## 6. Late-arriving data and recalculation

A July event delivered in an August batch updates July after watermark and
replay rules accept it. The recalculated result retains audit metadata.

## 7. Reporting grain and rounding

Results are grouped by organization, software product, and calendar month.
Displayed percentages round to one decimal place after aggregation.
