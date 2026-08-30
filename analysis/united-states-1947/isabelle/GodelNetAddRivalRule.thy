(* Adversarial evidence for `step-one-repair.md`.

   This file answers the strongest objection to the repaired formalization:
   that the proposal-validity rule was written so that Goedel's step one would
   come out load-bearing, which would make the result an artifact of the
   encoding rather than a fact about the argument.

   PROBE 1 (Nitpick, diagnostic). Runs the full theory with show_consts so the
   model can be inspected rather than merely counted. A theory satisfied only
   by a degenerate model says nothing.

   PROBE 2 (kernel proof). `rival_pvr_inconsistency` shows that a proposal rule
   dropping the entrenchment check -- attempted AND is_amd AND sup_prop implies
   is_prop -- contradicts `comsp`, the conditional entrenchment clause, whenever
   the clause is in force and the amendment does not maintain equal suffrage.
   Any sufficient condition for proposal that is consistent with that necessary
   condition must therefore carry the entrenchment check. The disjunction in
   `pvr` is forced by Article V's proviso, not chosen to need step one.

   The proof is short, and its weight comes from what it rules out rather than
   from its depth. It does not show that step one is necessary; that claim rests
   on the independence probes in `GodelNetAddNoStep1.thy` and is a Nitpick
   diagnostic, not a proof. *)

theory GodelNetAddRivalRule
  imports GodelNetAddFull
begin

(* ===== PROBE 1: Full-model shape =====
   Nitpick with show_consts shows the actual model assignments. *)

lemma full_model_shape: "True"
  nitpick[satisfy, user_axioms, card time = 4, show_consts, timeout = 300] oops

(* ===== PROBE 2: Rival pvr without entrenchment check =====
   pvr_strong: attempted AND is_amd AND sup_prop -> is_prop
   No disjunction with in_force_omsp / maint_suf.
   If this + comsp + the step-two stipulations are consistent, then
   the disjunction in pvr is NOT forced. If they are INconsistent,
   then any sufficient condition for proposal MUST include the
   entrenchment check.

   We test this by asserting pvr_strong as an additional axiom and
   checking consistency. Actually -- the cleanest test is to check
   whether pvr_strong, comsp, and the step-two stipulations entail False.
   We only need the step-two facts that fire pvr_strong at t2:
   attempted amd2, is_amd amd2, sup_prop Congress amd2.
   Plus: in_force_omsp t1 (it starts in force) and amd2_not_maint_suf_t2.
   If in_force_omsp remains true at t2, pvr_strong gives is_prop amd2 t2,
   but comsp gives NOT is_prop amd2 t2. Contradiction. *)

lemma rival_pvr_inconsistency:
  assumes pvr_strong: "\<forall>\<phi> t. attempted \<phi> t \<and> is_amd \<phi> t \<and>
            (\<forall>g. is_leg g t \<longrightarrow> sup_prop g \<phi> t) \<longrightarrow> is_prop \<phi> t"
  assumes comsp_holds: "\<forall>\<phi> t. in_force_omsp t \<and> \<not> maint_suf \<phi> t \<longrightarrow> \<not> is_prop \<phi> t"
  assumes att: "attempted amd2 t2" and amd: "is_amd amd2 t2"
  assumes sup: "\<forall>g. is_leg g t2 \<longrightarrow> sup_prop g amd2 t2"
  assumes notsuf: "\<not> maint_suf amd2 t2"
  assumes ifo: "in_force_omsp t2"
  shows "False"
proof -
  from pvr_strong att amd sup have "is_prop amd2 t2" by blast
  moreover from comsp_holds ifo notsuf have "\<not> is_prop amd2 t2" by blast
  ultimately show False by contradiction
qed

end
