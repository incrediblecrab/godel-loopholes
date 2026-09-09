theory GodelNetAddCausalityAudit
  imports GodelNetAddCore
begin

text \<open>
  This audit imports only the 39-axiom core, not the step-one extension.
  Kernel lemmas and bounded model-finder probes are kept separate. No new
  constitutional axioms, transition relation, or persistence rule is added.
\<close>

lemma audit_amd2_legislative_support:
  "\<forall>g. is_leg g t2 \<longrightarrow> sup_prop g amd2 t2"
  using Con_Leg_t2 sup_prop_amd2_t2 unique_is_leg
  unfolding Defs by blast

lemma audit_amd2_proposed_iff_clause_off:
  "is_prop amd2 t2 \<longleftrightarrow> \<not> in_force_omsp t2"
proof
  assume "is_prop amd2 t2"
  then show "\<not> in_force_omsp t2"
    using comsp_global amd2_not_maint_suf_t2
    unfolding Defs by blast
next
  assume "\<not> in_force_omsp t2"
  then show "is_prop amd2 t2"
    using amd2_attempted_t2 is_amd_amd2_t2
      audit_amd2_legislative_support pvr_elim
    by (auto simp: local_valid_def)
qed

lemma audit_t2_successor:
  "succ t2 t \<longleftrightarrow> t = t3"
  by (cases t)
    (simp_all add: Nt2_s_t1 Nt2_s_t2 t2_s_t3 Nt2_s_te)

lemma audit_t2_next:
  "tnext \<phi> t2 \<longleftrightarrow> \<phi> t3"
  by (simp add: tnext_def audit_t2_successor)

lemma audit_amd2_ratified_iff_proposed:
  "is_rat amd2 t3 \<longleftrightarrow> is_prop amd2 t2"
proof
  assume rat: "is_rat amd2 t3"
  have rule: "\<not> is_prop amd2 t2 \<longrightarrow> \<not> tnext (is_rat amd2) t2"
    using opr_global
    unfolding global_valid_def tallB_s_def tall_s_def timp_def tneg_def
    by blast
  show "is_prop amd2 t2"
    using rat rule audit_t2_next by blast
next
  assume proposed: "is_prop amd2 t2"
  have "tnext (is_rat amd2) t2"
    using proposed amd2_sup_rat_t2 psr_global
    unfolding global_valid_def local_valid_def tallB_s_def tall_s_def
      timp_def tand_def
    by blast
  then show "is_rat amd2 t3"
    by (simp only: audit_t2_next)
qed

lemma audit_clause_on_blocks_amd2:
  assumes "in_force_omsp t2"
  shows "\<not> is_prop amd2 t2 \<and> \<not> is_rat amd2 t3"
  using assms audit_amd2_proposed_iff_clause_off
    audit_amd2_ratified_iff_proposed by blast

lemma audit_amd2_content_implies_dictatorship:
  "amd2 t \<Longrightarrow> Dictatorship t"
  unfolding amd2_def Dictatorship_def local_valid_def tand_def by blast

lemma audit_clause_off_entails_dictatorship:
  assumes "\<not> in_force_omsp t2"
  shows "Dictatorship t3"
proof -
  have "is_rat amd2 t3"
    using assms audit_amd2_proposed_iff_clause_off
      audit_amd2_ratified_iff_proposed by blast
  then have "amd2 t3"
    using rv_global
    unfolding global_valid_def tallB_s_def tall_s_def timp_def
    by blast
  then show ?thesis
    using audit_amd2_content_implies_dictatorship by blast
qed

lemma audit_no_dictatorship_requires_clause_on:
  "\<not> Dictatorship t3 \<Longrightarrow> in_force_omsp t2"
  using audit_clause_off_entails_dictatorship by blast

lemma audit_core_unguarded_rule_forces_clause_off:
  assumes "\<forall>\<phi> t. attempted \<phi> t \<and> is_amd \<phi> t \<and>
    (\<forall>g. is_leg g t \<longrightarrow> sup_prop g \<phi> t) \<longrightarrow> is_prop \<phi> t"
  shows "\<not> in_force_omsp t2"
proof -
  have "is_prop amd2 t2"
    using assms amd2_attempted_t2 is_amd_amd2_t2 audit_amd2_legislative_support
    unfolding local_valid_def by blast
  then show ?thesis
    using audit_amd2_proposed_iff_clause_off by blast
qed

text \<open>
  Deleting step-one axioms is not the same operation as asserting that no
  repeal occurs. The first probe explicitly excludes the scheduled repeal
  attempt and ratification. A counterexample has the clause off anyway;
  the preceding kernel lemma then entails dictatorship in that assignment.
\<close>

lemma audit_no_repeal_event_does_not_supply_frame:
  assumes "\<not> attempted amd1a t1" "\<not> is_rat amd1a t2"
  shows "in_force_omsp t2"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

text \<open>
  The next three probes keep the clause on at every time and prohibit every
  ratification, not merely the repeal. They test both dictatorship outcomes
  and, separately, the presidential concentration defined by amd2. These are
  assignments satisfying the core, not lawful execution traces.
\<close>

lemma audit_clause_on_no_ratification_does_not_exclude_dictatorship:
  assumes "\<forall>t. in_force_omsp t"
    and "\<forall>\<phi> t. \<not> is_rat \<phi> t"
    and "\<not> attempted amd1a t1"
  shows "\<not> Dictatorship t3"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

lemma audit_clause_on_no_ratification_does_not_exclude_amd2_content:
  assumes "\<forall>t. in_force_omsp t"
    and "\<forall>\<phi> t. \<not> is_rat \<phi> t"
    and "\<not> attempted amd1a t1"
  shows "\<not> amd2 t3"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

lemma audit_clause_on_no_ratification_does_not_force_dictatorship:
  assumes "\<forall>t. in_force_omsp t"
    and "\<forall>\<phi> t. \<not> is_rat \<phi> t"
    and "\<not> attempted amd1a t1"
  shows "Dictatorship t3"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

text \<open>
  The following are propositional schemata over fresh Boolean variables.
  Their proofs use only their displayed premises. The probes retain the
  core axioms so that Nitpick also checks ambient satisfiability; none of
  these fresh Boolean variables denotes a constitutional-model constant.
\<close>

lemma audit_abstract_sufficient_necessary_conflict:
  fixes A M S F H V :: bool
  assumes sufficient: "A \<and> M \<and> S \<longrightarrow> V"
    and necessary: "F \<and> \<not> H \<longrightarrow> \<not> V"
    and trigger: "A" "M" "S" "F" "\<not> H"
  shows False
  using assms by blast

lemma audit_abstract_necessary_guard:
  fixes F H V :: bool
  shows "(F \<and> \<not> H \<longrightarrow> \<not> V) \<longleftrightarrow> (V \<longrightarrow> \<not> F \<or> H)"
  by blast

lemma audit_abstract_sufficient_antecedent_requires_guard:
  fixes C F H V :: bool
  assumes "C \<longrightarrow> V" "F \<and> \<not> H \<longrightarrow> \<not> V"
  shows "C \<longrightarrow> \<not> F \<or> H"
  using assms by blast

lemma audit_abstract_stricter_rule_witness:
  "\<exists>A M S F H V E :: bool.
    A \<and> M \<and> S \<and> (\<not> F \<or> H) \<and> \<not> V \<and>
    (F \<and> \<not> H \<longrightarrow> \<not> V) \<and>
    (A \<and> M \<and> S \<and> (\<not> F \<or> H) \<and> E \<longrightarrow> V)"
  by blast

lemma audit_abstract_necessity_does_not_force_sufficiency:
  fixes A M S F H V :: bool
  assumes "F \<and> \<not> H \<longrightarrow> \<not> V"
  shows "A \<and> M \<and> S \<and> (\<not> F \<or> H) \<longrightarrow> V"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

lemma audit_abstract_rival_rules_without_forbidden_trigger:
  fixes A M S F H V :: bool
  assumes "A \<and> M \<and> S \<longrightarrow> V"
    and "F \<and> \<not> H \<longrightarrow> \<not> V"
  shows False
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

end
