# Signatory sample: search log and honest result

Objective 2/3, Step 4. What a wider search sweep, run across roughly 18
individual WA councils plus the general searches behind `EXECUTION_PROMPT.md`,
actually found, and what it did not.

## What the sweep covered

Beyond the general searches for a master signatory list (`EXECUTION_PROMPT.md`
already recorded that none is published), this pass searched, council by
council: City of Fremantle, City of Cockburn, City of Busselton, City of
Albany, City of Bunbury, City of Rockingham, City of Kalamunda, City of
Armadale, Shire of Augusta-Margaret River, Shire of Denmark, City of Swan,
City of Joondalup, and Shire of Harvey (carried over from the earlier
scoping pass). For each, the search asked whether the council is a WALGA
Declaration signatory and, if so, when it signed.

## The honest result

**Signatory status is usually easy to confirm; the signing date almost
never is.** Six councils' own web pages state signatory status outright
(`data/signatory-sample.csv`: Harvey, Kalamunda, Busselton, Denmark
weakly, plus two more that turned out to be about a different instrument
entirely, Vincent and Albany). Only one, Shire of Harvey, has a signing
date with even medium confidence, corroborated across two independent
references (a Council Action Register entry and confirmation an Ordinary
Council Meeting was held on that date), and even that was not confirmed by
directly reading the primary minutes PDF, which this session's tools could
not fetch in full (file size limit). City of Kalamunda's often-repeated 10
August 2021 date turned out to be unconfirmed on inspection: it appears
consistently in web search summaries but was not present when the cited
page itself was fetched directly. That discrepancy is exactly the kind of
thing evidence discipline exists to catch, so the date is flagged, not
used.

**Two genuine conflation cases turned up**, which is useful in its own
right. City of Vincent's council endorsed WALGA's 2018 Policy Statement,
not the Declaration, the same distinction `EXECUTION_PROMPT.md` corrected
for this project as a whole. City of Albany has its own, separately
authored "Climate Change Action Declaration" (first adopted October 2020
after a Youth Advisory Council petition), confirmed by a direct page fetch
to be a different instrument from WALGA's Declaration, not a signature on
it. Both are recorded in `data/signatory-sample.csv` as excluded, with the
reason stated, rather than silently dropped. They are also a live
demonstration of why coding item P12 (`coding-framework.md`) exists.

**No confirmed non-signatory was found.** Four councils (Swan, Joondalup,
Cockburn, Bunbury) returned no public statement either way. That is
absence of evidence, not evidence of absence: it means a general web
search did not surface a statement, not that the council has not signed.
Building Objective 3's comparison group needs a positive confirmation of
non-signatory status, which this method cannot supply.

## What this means for Objectives 2 and 3 as designed

The within-council before/after design (Objective 2) needs a sample of
councils with confirmed signing dates. This pass found one, at medium
confidence. The cross-council comparison design (Objective 3) needs
confirmed non-signatories. This pass found none. Neither objective can run
on a defensible sample using general web search alone, which is the same
structural limit flagged before this sweep started, now confirmed by
running it rather than assumed. See `README.md` for the resulting
recommendation and the decision this leaves for Ris.
