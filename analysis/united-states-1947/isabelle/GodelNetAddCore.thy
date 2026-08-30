(* ------------------------------------------------------------------------
   GodelNetAddCore.thy

   A NEW formalization addressing three defects in the Zahoransky & Benzmueller
   (Z&B) model of Goedel's claim:

     1. in_force is separated from compliance: in_force_omsp tracks whether
        the entrenchment clause is legally operative, distinct from whether
        actors are obeying it.

     2. attempted vs. valid proposal are distinguished: attempted marks a
        proposal put forward; is_prop marks one that passes all preconditions.

     3. amd2_prop_t2 is NO LONGER AN AXIOM. It is derived in GodelNetAddFull
        from preconditions, including the fact that step one has repealed the
        entrenchment clause.

   This file contains infrastructure, global rules, government axioms,
   step-two stipulations (the CONDITIONS for step two, not its validity),
   and the noDictatorship theorems for t1 and t2.

   GodelNetAddFull.thy adds the step-one axioms and derives everything.
   GodelNetAddNoStep1.thy imports this file WITHOUT step one and probes
   whether Dictatorship_t3 is still entailed.

   THE BASELINE (GodelCore.thy + GodelConstitution.thy) IS NOT TOUCHED.
   verify.sh checks it independently.

   Vantage: United States, December 5, 1947.
   ------------------------------------------------------------------------ *)

theory GodelNetAddCore
  imports Main
begin

(* ===== DATA TYPES: identical to Z&B ===== *)

datatype g = Congress | P | Courts

datatype time = t1 | t2 | t3 | te

type_synonym \<sigma> = "time \<Rightarrow> bool"

(* ===== LIFTED OPERATORS: identical to Z&B ===== *)

definition tneg :: "\<sigma>\<Rightarrow>\<sigma>" ("\<^bold>\<not>_"[52]53)
  where "\<^bold>\<not>\<phi> \<equiv> \<lambda>t. \<not>\<phi>(t)"
definition tand :: "\<sigma>\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>" (infixr "\<^bold>\<and>" 51)
  where "\<phi>\<^bold>\<and>\<psi> \<equiv> \<lambda>t. \<phi>(t)\<and>\<psi>(t)"
definition tor :: "\<sigma>\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>" (infixr "\<^bold>\<or>" 50)
  where "\<phi>\<^bold>\<or>\<psi> \<equiv> \<lambda>t. \<phi>(t)\<or>\<psi>(t)"
definition timp :: "\<sigma>\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>" (infixr "\<^bold>\<longrightarrow>" 49)
  where "\<phi>\<^bold>\<longrightarrow>\<psi> \<equiv> \<lambda>t. \<phi>(t)\<longrightarrow>\<psi>(t)"
definition tequ :: "\<sigma>\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>" (infixr "\<^bold>\<longleftrightarrow>" 48)
  where "\<phi>\<^bold>\<longleftrightarrow>\<psi> \<equiv> \<lambda>t. \<phi>(t)\<longleftrightarrow>\<psi>(t)"

definition teq :: "g\<Rightarrow>g\<Rightarrow>\<sigma>" (infixr "\<^bold>=" 40)
  where "\<phi>\<^bold>=\<psi> \<equiv> \<lambda>t. \<phi>=\<psi>"
definition tneq :: "g\<Rightarrow>g\<Rightarrow>\<sigma>" (infixr "\<^bold>\<noteq>" 40)
  where "\<phi>\<^bold>\<noteq>\<psi> \<equiv> \<lambda>t. \<not>(\<phi>=\<psi>)"

definition tall_g :: "(g\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" ("\<^bold>\<forall>\<^sub>g")
  where "\<^bold>\<forall>\<^sub>g \<Phi> \<equiv> \<lambda>t. \<forall>x. \<Phi>(x)(t)"
definition tallB_g :: "(g\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" (binder "\<^bold>\<forall>\<^sub>g" [8]9)
  where "\<^bold>\<forall>\<^sub>g x. \<phi>(x) \<equiv> \<^bold>\<forall>\<^sub>g \<phi>"

definition texi_g :: "(g\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" ("\<^bold>\<exists>\<^sub>g")
  where "\<^bold>\<exists>\<^sub>g \<Phi> \<equiv> \<lambda>t. \<exists>x. \<Phi>(x)(t)"
definition texiB_g :: "(g\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" (binder "\<^bold>\<exists>\<^sub>g" [8]9)
  where "\<^bold>\<exists>\<^sub>g x. \<phi>(x) \<equiv> \<^bold>\<exists>\<^sub>g \<phi>"

definition tall_s :: "(\<sigma>\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" ("\<^bold>\<forall>\<^sub>s")
  where "\<^bold>\<forall>\<^sub>s \<Phi> \<equiv> \<lambda>t. \<forall>\<phi>. \<Phi>(\<phi>)(t)"
definition tallB_s :: "(\<sigma>\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" (binder "\<^bold>\<forall>\<^sub>s" [8]9)
  where "\<^bold>\<forall>\<^sub>s \<phi>. \<Phi>(\<phi>) \<equiv> \<^bold>\<forall>\<^sub>s \<Phi>"

definition texi_s :: "(\<sigma>\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" ("\<^bold>\<exists>\<^sub>s")
  where "\<^bold>\<exists>\<^sub>s \<Phi> \<equiv> \<lambda>t. \<exists>\<phi>. \<Phi>(\<phi>)(t)"
definition texiB_s :: "(\<sigma>\<Rightarrow>\<sigma>)\<Rightarrow>\<sigma>" (binder "\<^bold>\<exists>\<^sub>s" [8]9)
  where "\<^bold>\<exists>\<^sub>s \<phi>. \<Phi>(\<phi>) \<equiv> \<^bold>\<exists>\<^sub>s \<Phi>"

(* ===== SUCCESSOR RELATION: identical to Z&B ===== *)

consts succ :: "time\<Rightarrow>time\<Rightarrow>bool"

axiomatization where
  t1_s_t2:  "succ t1 t2" and
  t2_s_t3:  "succ t2 t3" and
  t3_s_te:  "succ t3 te" and
  te_s_te:  "succ te te" and
  Nt1_s_t1: "\<not>(succ t1 t1)" and
  Nt1_s_t3: "\<not>(succ t1 t3)" and
  Nt1_s_te: "\<not>(succ t1 te)" and
  Nt2_s_t1: "\<not>(succ t2 t1)" and
  Nt2_s_t2: "\<not>(succ t2 t2)" and
  Nt2_s_te: "\<not>(succ t2 te)" and
  Nt3_s_t1: "\<not>(succ t3 t1)" and
  Nt3_s_t2: "\<not>(succ t3 t2)" and
  Nt3_s_t3: "\<not>(succ t3 t3)" and
  Nte_s_t1: "\<not>(succ te t1)" and
  Nte_s_t2: "\<not>(succ te t2)" and
  Nte_s_t3: "\<not>(succ te t3)"

definition tnext :: "\<sigma>\<Rightarrow>\<sigma>" ("\<^bold>X_")
  where "\<^bold>X\<phi> \<equiv> (\<lambda>t. \<forall>t'. ((succ t t') \<longrightarrow> \<phi> t'))"

(* ===== VALIDITY: identical to Z&B ===== *)

definition global_valid :: "\<sigma> \<Rightarrow> bool" ("\<lfloor>_\<rfloor>"[7]8)
  where "\<lfloor>\<phi>\<rfloor> \<equiv> \<forall>t. \<phi> t"
definition local_valid :: "\<sigma>\<Rightarrow>time \<Rightarrow> bool" ("\<lfloor>_\<rfloor>_" [9]10)
  where "\<lfloor>\<phi>\<rfloor>t \<equiv> \<phi> t"

named_theorems Defs
declare
  tneg_def[Defs] tand_def[Defs]
  tor_def[Defs] timp_def[Defs] tequ_def[Defs]
  teq_def[Defs] tneq_def[Defs]
  tall_g_def[Defs] tallB_g_def[Defs]
  texi_g_def[Defs] texiB_g_def[Defs]
  tall_s_def[Defs] tallB_s_def[Defs]
  texi_s_def[Defs] texiB_s_def[Defs]
  tnext_def[Defs]
  global_valid_def[Defs] local_valid_def[Defs]

(* ===== CONSTANTS ===== *)

consts
  is_leg :: "g\<Rightarrow>\<sigma>"
  is_exe :: "g\<Rightarrow>\<sigma>"
  is_jud :: "g\<Rightarrow>\<sigma>"

consts
  is_amd    :: "\<sigma>\<Rightarrow>\<sigma>"
  is_prop   :: "\<sigma>\<Rightarrow>\<sigma>"
  is_rat    :: "\<sigma>\<Rightarrow>\<sigma>"
  sup_prop  :: "g\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>"
  sup_rat   :: "\<sigma>\<Rightarrow>\<sigma>"
  maint_suf :: "\<sigma>\<Rightarrow>\<sigma>"

(* NEW CONSTANTS.
   in_force_omsp tracks whether the entrenchment clause is in force.
   attempted tracks whether an amendment has been put forward for proposal.
   These are the two predicates the Z&B model lacks. *)
consts
  in_force_omsp :: "\<sigma>"
  attempted     :: "\<sigma>\<Rightarrow>\<sigma>"

(* ===== UNIQUENESS: identical to Z&B ===== *)

axiomatization where
  unique_is_leg: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_leg g1)\<^bold>\<and>(is_leg g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>" and
  unique_is_exe: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_exe g1)\<^bold>\<and>(is_exe g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>" and
  unique_is_jud: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_jud g1)\<^bold>\<and>(is_jud g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>"

definition Dictatorship :: "\<sigma>"
  where "Dictatorship \<equiv> \<lambda>t. \<exists>d. \<lfloor>(is_leg d) \<^bold>\<and> (is_exe d) \<^bold>\<and> (is_jud d)\<rfloor>t"

(* ===== ABBREVIATIONS ===== *)

(* From Z&B, unchanged: *)
abbreviation oap :: "\<sigma>"
  where "oap \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (\<^bold>\<not>(is_amd \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(is_prop \<phi>))"

abbreviation osp :: "\<sigma>"
  where "osp \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. \<^bold>\<forall>\<^sub>g g.(is_leg g)\<^bold>\<longrightarrow>((\<^bold>\<not>(sup_prop g \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(is_prop \<phi>)))"

abbreviation opr :: "\<sigma>"
  where "opr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (\<^bold>\<not>(is_prop \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(\<^bold>X(is_rat \<phi>)))"

abbreviation osr :: "\<sigma>"
  where "osr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. \<^bold>\<forall>\<^sub>g g. (\<^bold>\<not>(sup_rat \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(\<^bold>X(is_rat \<phi>)))"

abbreviation psr :: "\<sigma>"
  where "psr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (is_prop \<phi> \<^bold>\<and> (sup_rat \<phi>))\<^bold>\<longrightarrow> (\<^bold>X(is_rat \<phi>))"

abbreviation rv :: "\<sigma>"
  where "rv \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (is_rat \<phi>) \<^bold>\<longrightarrow> \<phi>"

(* NEW: conditional entrenchment clause.
   Z&B's omsp is unconditional: nothing that fails to maintain suffrage can
   be proposed. comsp conditions this on the clause being in force. When
   in_force_omsp is false, the constraint is lifted. *)
abbreviation comsp :: "\<sigma>"
  where "comsp \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (in_force_omsp \<^bold>\<and> (\<^bold>\<not>(maint_suf \<phi>))) \<^bold>\<longrightarrow> (\<^bold>\<not>(is_prop \<phi>))"

(* NEW: proposal validity rule.
   In Z&B, is_prop is asserted directly. Here an attempted amendment that
   is an amendment, has legislative support, and either the entrenchment
   clause is not in force OR the amendment maintains suffrage, becomes
   a valid proposal. This is what lets amd2_prop_t2 be DERIVED. *)
abbreviation pvr :: "\<sigma>"
  where "pvr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>.
    ((attempted \<phi>) \<^bold>\<and> (is_amd \<phi>) \<^bold>\<and>
     (\<^bold>\<forall>\<^sub>g g. (is_leg g) \<^bold>\<longrightarrow> (sup_prop g \<phi>)) \<^bold>\<and>
     ((\<^bold>\<not> in_force_omsp) \<^bold>\<or> (maint_suf \<phi>)))
    \<^bold>\<longrightarrow> (is_prop \<phi>)"

(* ===== DEFINITIONS ===== *)

(* The amendment repealing the entrenchment clause. Its CONTENT is that the
   entrenchment clause is not in force. When ratified and rv applies, this
   directly yields NOT in_force_omsp at the ratification time. This separates
   the amendment event from the compliance question: the model no longer
   conflates "clause is in force" with "actors obey it".

   Contrast with Z&B's amd1a = EXISTS phi. NOT(maint_suf phi) AND is_prop phi,
   which is the NEGATION of the constraint itself and hence conflates the
   repeal with a violation. *)
definition amd1a :: "\<sigma>"
  where "amd1a \<equiv> \<^bold>\<not> in_force_omsp"

(* The amendment installing dictatorship -- same as Z&B. *)
definition amd2 :: "\<sigma>" where "amd2 \<equiv> is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P"

(* ===== AXIOMS: GOVERNMENT AT t1 ===== *)

axiomatization where
  Con_Leg_t1: "\<lfloor>is_leg Congress\<rfloor>t1" and
  P_Exe_t1:   "\<lfloor>is_exe P\<rfloor>t1" and
  Cou_Jud_t1: "\<lfloor>is_jud Courts\<rfloor>t1"

(* Government propagation from t1 to t2 only. At t3, amd2 takes over. *)
axiomatization where
  XCon_Leg_t1: "\<lfloor>\<^bold>X(is_leg Congress)\<rfloor>t1" and
  XP_Exe_t1:   "\<lfloor>\<^bold>X(is_exe P)\<rfloor>t1" and
  XCou_Jud_t1: "\<lfloor>\<^bold>X(is_jud Courts)\<rfloor>t1"

(* ===== AXIOMS: CONSTITUTIONAL RULES (global) =====

   Z&B asserts each rule at t1 and propagates it via X-axioms. Making rules
   global is equivalent but simpler: the RULES do not change across time.
   What changes is the FACT about whether the entrenchment clause is in force,
   which is tracked by in_force_omsp rather than by omitting an axiom. *)

axiomatization where
  oap_global:   "\<lfloor>oap\<rfloor>" and
  osp_global:   "\<lfloor>osp\<rfloor>" and
  comsp_global: "\<lfloor>comsp\<rfloor>" and
  opr_global:   "\<lfloor>opr\<rfloor>" and
  rv_global:    "\<lfloor>rv\<rfloor>" and
  osr_global:   "\<lfloor>osr\<rfloor>" and
  psr_global:   "\<lfloor>psr\<rfloor>" and
  pvr_global:   "\<lfloor>pvr\<rfloor>"

(* ===== AXIOM: INITIAL STATE ===== *)

(* The entrenchment clause IS in force at t1. This is the one bit that Z&B
   represent by the PRESENCE of the omsp axiom. Here it is an explicit fact
   about a separate predicate. *)
axiomatization where
  in_force_omsp_t1: "\<lfloor>in_force_omsp\<rfloor>t1"

(* ===== AXIOMS: STEP-TWO STIPULATIONS =====

   These are the CONDITIONS for the dictatorship amendment: it is attempted,
   it is an amendment, Congress supports it, it does not maintain suffrage,
   and the states support ratification. NONE of these asserts is_prop amd2.
   Whether amd2 is validly proposed depends on whether the entrenchment
   clause has been repealed, which depends on step one. *)

axiomatization where
  amd2_attempted_t2:      "\<lfloor>attempted amd2\<rfloor>t2" and
  is_amd_amd2_t2:         "\<lfloor>is_amd amd2\<rfloor>t2" and
  sup_prop_amd2_t2:       "\<lfloor>sup_prop Congress amd2\<rfloor>t2" and
  amd2_not_maint_suf_t2:  "\<lfloor>\<^bold>\<not>(maint_suf amd2)\<rfloor>t2" and
  amd2_sup_rat_t2:        "\<lfloor>sup_rat amd2\<rfloor>t2"

(* ===== LEMMAS: GOVERNMENT ===== *)

lemma only_Con_Leg_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_leg g)\<^bold>\<longrightarrow>(g \<^bold>= Congress)\<rfloor>t1"
  unfolding Defs using unique_is_leg Con_Leg_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def
                tand_def teq_def timp_def)

lemma only_P_Exe_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_exe g)\<^bold>\<longrightarrow>(g \<^bold>= P)\<rfloor>t1"
  unfolding Defs using unique_is_exe P_Exe_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def
                tand_def teq_def timp_def)

lemma only_Cou_Jud_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_jud g)\<^bold>\<longrightarrow>(g \<^bold>= Courts)\<rfloor>t1"
  unfolding Defs using unique_is_jud Cou_Jud_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def
                tand_def teq_def timp_def)

theorem noDictatorship_t1: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t1"
  unfolding Defs using only_Con_Leg_t1 only_P_Exe_t1 only_Cou_Jud_t1
  by (metis (no_types, lifting) Dictatorship_def g.distinct(1) local_valid_def
      tallB_g_def tall_g_def tand_def teq_def timp_def)

(* ===== t2 GOVERNMENT: from X-propagation ===== *)

lemma Con_Leg_t2: "\<lfloor>is_leg Congress\<rfloor>t2"
  unfolding Defs using XCon_Leg_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma P_Exe_t2: "\<lfloor>is_exe P\<rfloor>t2"
  unfolding Defs using XP_Exe_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma Cou_Jud_t2: "\<lfloor>is_jud Courts\<rfloor>t2"
  using XCou_Jud_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma only_Con_Leg_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_leg g)\<^bold>\<longrightarrow>(g \<^bold>= Congress)\<rfloor>t2"
  using unique_is_leg Con_Leg_t2 global_valid_def local_valid_def tallB_g_def
        tall_g_def tand_def teq_def timp_def
  by simp

lemma only_P_Exe_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_exe g)\<^bold>\<longrightarrow>(g \<^bold>= P)\<rfloor>t2"
  unfolding Defs using unique_is_exe P_Exe_t2
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def
                tand_def teq_def timp_def)

lemma only_Cou_Jud_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_jud g)\<^bold>\<longrightarrow>(g \<^bold>= Courts)\<rfloor>t2"
  unfolding Defs using unique_is_jud Cou_Jud_t2
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def
                tand_def teq_def timp_def)

theorem noDictatorship_t2: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t2"
  unfolding Defs using only_Con_Leg_t2 only_P_Exe_t2 only_Cou_Jud_t2
            Dictatorship_def
  by (metis (mono_tags, lifting) g.distinct(3) local_valid_def tallB_g_def
      tall_g_def tand_def teq_def timp_def)

(* Elimination form of pvr for use in proofs. The schematic variables let
   Isabelle match phi and t when the lemma is applied. *)
lemma pvr_elim:
  assumes "attempted \<phi> t" "is_amd \<phi> t"
  assumes "\<forall>g. is_leg g t \<longrightarrow> sup_prop g \<phi> t"
  assumes "\<not> in_force_omsp t \<or> maint_suf \<phi> t"
  shows "is_prop \<phi> t"
  using assms pvr_global
  unfolding Defs by blast

end
