(* ------------------------------------------------------------------------
   GodelConstitution.thy

   Replication of:
     Valeria Zahoransky, "Modelling the US Constitution in HOL", BSc thesis,
     Freie Universitaet Berlin, 2019 (supervisor: Christoph Benzmueller), and
     Zahoransky & Benzmueller, "Modelling the US Constitution to establish
     constitutional dictatorship", MIREL 2019 @ JURIX, CEUR vol. 2632.

   The authors publish no .thy file. This theory is transcribed by hand from
   the thesis PDF, sections 4.2 and 4.3. Section numbers in the comments below
   refer to the thesis.

   The argument being formalised is Guerra-Pujol's reconstruction of Goedel's
   claim, NOT Goedel's own reasoning, which survives in no source. The authors
   state this themselves in their second paragraph.

   Replication targets, in order:
     theorem noDictatorship_t1   -- no dictatorship under the 1947 Constitution
     theorem noDictatorship_t2   -- none after Article V is amended
     theorem Dictatorship_t3     -- dictatorship, by lawful steps only
   ------------------------------------------------------------------------ *)

theory ConsistencyCheck
  imports Main
begin

(* ---------------- 4.2.1 Data types ---------------- *)

(* Governmental institutions. Courts stands for the Supreme Court together
   with the inferior courts Congress may ordain and establish, Art. III sec. 1. *)
datatype g = Congress | P | Courts

(* t1 holds the 1947 Constitution; t2 holds it with Art. V amended so that
   amendments need not maintain the states' equal suffrage in the Senate;
   t3 holds the Constitution upholding dictatorship. te is a technical
   end-of-time successor, needed so that t3 has a successor and the axiom
   X opr at t2 does not become inconsistent. *)
datatype time = t1 | t2 | t3 | te

type_synonym \<sigma> = "time \<Rightarrow> bool"

(* ---------------- 4.2.2 Lifted operators ---------------- *)

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

(* The successor relation. Called succ rather than pred to stress that X
   speaks about a future instance of time. *)
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

(* ---------------- 4.2.3 Validity ---------------- *)

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

(* ---------------- 4.3.1 Preliminaries ---------------- *)

consts
  is_leg :: "g\<Rightarrow>\<sigma>"   \<comment> \<open>g is the legislative\<close>
  is_exe :: "g\<Rightarrow>\<sigma>"   \<comment> \<open>g is the executive\<close>
  is_jud :: "g\<Rightarrow>\<sigma>"   \<comment> \<open>g is the judiciary\<close>

axiomatization where
  unique_is_leg: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_leg g1)\<^bold>\<and>(is_leg g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>" and
  unique_is_exe: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_exe g1)\<^bold>\<and>(is_exe g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>" and
  unique_is_jud: "\<lfloor>\<^bold>\<forall>\<^sub>g g1. \<^bold>\<forall>\<^sub>g g2. (((is_jud g1)\<^bold>\<and>(is_jud g2))\<^bold>\<longrightarrow>(g1 \<^bold>= g2))\<rfloor>"

definition Dictatorship :: "\<sigma>"
  where "Dictatorship \<equiv> \<lambda>t. \<exists>d. \<lfloor>(is_leg d) \<^bold>\<and> (is_exe d) \<^bold>\<and> (is_jud d)\<rfloor>t"

consts
  is_amd    :: "\<sigma>\<Rightarrow>\<sigma>"       \<comment> \<open>phi is an amendment\<close>
  is_prop   :: "\<sigma>\<Rightarrow>\<sigma>"       \<comment> \<open>phi is proposed\<close>
  is_rat    :: "\<sigma>\<Rightarrow>\<sigma>"       \<comment> \<open>phi is ratified\<close>
  sup_prop  :: "g\<Rightarrow>\<sigma>\<Rightarrow>\<sigma>"    \<comment> \<open>phi has support by g to be proposed\<close>
  sup_rat   :: "\<sigma>\<Rightarrow>\<sigma>"       \<comment> \<open>phi has support to be ratified\<close>
  maint_suf :: "\<sigma>\<Rightarrow>\<sigma>"       \<comment> \<open>phi maintains suffrage in Senate for all states\<close>

abbreviation oap :: "\<sigma>"
  where "oap \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (\<^bold>\<not>(is_amd \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(is_prop \<phi>))"

abbreviation osp :: "\<sigma>"
  where "osp \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. \<^bold>\<forall>\<^sub>g g.(is_leg g)\<^bold>\<longrightarrow>((\<^bold>\<not>(sup_prop g \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(is_prop \<phi>)))"

abbreviation omsp :: "\<sigma>"
  where "omsp \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (\<^bold>\<not>(maint_suf \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(is_prop \<phi>))"

abbreviation opr :: "\<sigma>"
  where "opr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (\<^bold>\<not>(is_prop \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(\<^bold>X(is_rat \<phi>)))"

abbreviation osr :: "\<sigma>"
  where "osr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. \<^bold>\<forall>\<^sub>g g. (\<^bold>\<not>(sup_rat \<phi>))\<^bold>\<longrightarrow>(\<^bold>\<not>(\<^bold>X(is_rat \<phi>)))"

abbreviation psr :: "\<sigma>"
  where "psr \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (is_prop \<phi> \<^bold>\<and> (sup_rat \<phi>))\<^bold>\<longrightarrow> (\<^bold>X(is_rat \<phi>))"

abbreviation rv :: "\<sigma>"
  where "rv \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (is_rat \<phi>) \<^bold>\<longrightarrow> \<phi>"

(* ---------------- 4.3.2 Time instance t1 ---------------- *)

axiomatization where
  Con_Leg_t1: "\<lfloor>is_leg Congress\<rfloor>t1" and
  P_Exe_t1:   "\<lfloor>is_exe P\<rfloor>t1" and
  Cou_Jud_t1: "\<lfloor>is_jud Courts\<rfloor>t1"

axiomatization where
  oap_t1:  "\<lfloor>oap\<rfloor>t1" and
  osp_t1:  "\<lfloor>osp\<rfloor>t1" and
  omsp_t1: "\<lfloor>omsp\<rfloor>t1" and
  opr_t1:  "\<lfloor>opr\<rfloor>t1" and
  rv_t1:   "\<lfloor>rv\<rfloor>t1" and
  osr_t1:  "\<lfloor>osr\<rfloor>t1" and
  psr_t1:  "\<lfloor>psr\<rfloor>t1"

definition amd1a :: "\<sigma>"
  where "amd1a \<equiv> \<^bold>\<exists>\<^sub>s \<phi>. (\<^bold>\<not>(maint_suf \<phi>))\<^bold>\<and>((is_prop \<phi>))"
definition amd1b :: "\<sigma>"
  where "amd1b \<equiv> \<^bold>\<forall>\<^sub>s \<phi>. (is_prop \<phi>)\<^bold>\<longrightarrow> ((maint_suf \<phi>) \<^bold>\<or> \<^bold>\<not>(maint_suf \<phi>))"

axiomatization where
  amd1a_prop_t1:    "\<lfloor>is_prop amd1a\<rfloor>t1" and
  amd1a_sup_rat_t1: "\<lfloor>sup_rat amd1a\<rfloor>t1" and
  amd1b_prop_t1:    "\<lfloor>is_prop amd1b\<rfloor>t1" and
  amd1b_sup_rat_t1: "\<lfloor>sup_rat amd1b\<rfloor>t1"

axiomatization where
  XCon_Leg_t1: "\<lfloor>\<^bold>X(is_leg Congress)\<rfloor>t1" and
  XP_Exe_t1:   "\<lfloor>\<^bold>X(is_exe P)\<rfloor>t1" and
  XCou_Jud_t1: "\<lfloor>\<^bold>X(is_jud Courts)\<rfloor>t1"

(* Every property carries forward to t2 EXCEPT omsp. Note carefully: the
   amendment to Article V is implemented by the ABSENCE of an axiom
   "X omsp at t1", not by any amendment actually doing work. The authors
   acknowledge this in section 4.3.3 and defend it as unavoidable here. *)
axiomatization where
  Xoap_t1: "\<lfloor>\<^bold>X oap\<rfloor>t1" and
  Xosp_t1: "\<lfloor>\<^bold>X osp\<rfloor>t1" and
  Xopr_t1: "\<lfloor>\<^bold>X opr\<rfloor>t1" and
  Xrv_t1:  "\<lfloor>\<^bold>X rv\<rfloor>t1" and
  Xosr_t1: "\<lfloor>\<^bold>X osr\<rfloor>t1" and
  Xpsr_t1: "\<lfloor>\<^bold>X psr\<rfloor>t1"

lemma only_Con_Leg_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_leg g)\<^bold>\<longrightarrow>(g \<^bold>= Congress)\<rfloor>t1"
  unfolding Defs using unique_is_leg Con_Leg_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def tand_def teq_def timp_def)

lemma only_P_Exe_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_exe g)\<^bold>\<longrightarrow>(g \<^bold>= P)\<rfloor>t1"
  unfolding Defs using unique_is_exe P_Exe_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def tand_def teq_def timp_def)

lemma only_Cou_Jud_t1: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_jud g)\<^bold>\<longrightarrow>(g \<^bold>= Courts)\<rfloor>t1"
  unfolding Defs using unique_is_jud Cou_Jud_t1
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def tand_def teq_def timp_def)

theorem noDictatorship_t1: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t1"
  unfolding Defs using only_Con_Leg_t1 only_P_Exe_t1 only_Cou_Jud_t1
  by (metis (no_types, lifting) Dictatorship_def g.distinct(1) local_valid_def
      tallB_g_def tall_g_def tand_def teq_def timp_def)

(* ---------------- 4.3.3 Time instance t2 ---------------- *)

lemma Con_Leg_t2: "\<lfloor>is_leg Congress\<rfloor>t2"
  unfolding Defs using XCon_Leg_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma P_Exe_t2: "\<lfloor>is_exe P\<rfloor>t2"
  unfolding Defs using XP_Exe_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma Cou_Jud_t2: "\<lfloor>is_jud Courts\<rfloor>t2"
  using XCou_Jud_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma oap_t2: "\<lfloor>oap\<rfloor>t2" using Xoap_t1 local_valid_def tnext_def t1_s_t2 by auto
lemma osp_t2: "\<lfloor>osp\<rfloor>t2" using Xosp_t1 local_valid_def tnext_def t1_s_t2 by auto
lemma opr_t2: "\<lfloor>opr\<rfloor>t2" using Xopr_t1 local_valid_def tnext_def t1_s_t2 by auto
lemma rv_t2:  "\<lfloor>rv\<rfloor>t2"  using Xrv_t1  local_valid_def tnext_def t1_s_t2 by auto
lemma osr_t2: "\<lfloor>osr\<rfloor>t2" using Xosr_t1 local_valid_def tnext_def t1_s_t2 by auto
lemma psr_t2: "\<lfloor>psr\<rfloor>t2" using Xpsr_t1 local_valid_def tnext_def t1_s_t2 by auto

lemma amd1a_val_t2: "\<lfloor>amd1a\<rfloor>t2"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd1a)\<rfloor>t1"
    using amd1a_prop_t1 amd1a_sup_rat_t1 psr_t1 local_valid_def tallB_s_def
          tall_s_def tand_def timp_def tnext_def
    by auto
  thus "\<lfloor>amd1a\<rfloor>t2"
    using local_valid_def tallB_s_def tall_s_def timp_def tnext_def rv_t2 t1_s_t2
    by auto
qed

lemma amd1b_val_t2: "\<lfloor>amd1b\<rfloor>t2"
  unfolding Defs
  by (simp add: amd1b_def tallB_s_def tall_s_def timp_def tneg_def tor_def)

lemma amd1b_val_t2_2: "\<lfloor>amd1b\<rfloor>t2"
  unfolding Defs using amd1b_sup_rat_t1 amd1b_prop_t1 psr_t1 rv_t2
  by (simp add: amd1b_def tallB_s_def tall_s_def timp_def tneg_def tor_def)

lemma amd1b_val_t1: "\<lfloor>amd1b\<rfloor>t1"
  unfolding Defs
  by (simp add: amd1b_def tallB_s_def tall_s_def timp_def tneg_def tor_def)

lemma amd1b_val: "\<lfloor>amd1b\<rfloor>"
  unfolding Defs
  by (simp add: amd1b_def tallB_s_def tall_s_def timp_def tneg_def tor_def)

(* amd2 transfers all governmental power to the President. *)
definition amd2 :: "\<sigma>" where "amd2 \<equiv> is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P"

axiomatization where
  amd2_prop_t2:          "\<lfloor>is_prop amd2\<rfloor>t2" and
  amd2_sup_rat_t2:       "\<lfloor>sup_rat amd2\<rfloor>t2" and
  amd2_not_maint_suf_t2: "\<lfloor>\<^bold>\<not>(maint_suf amd2)\<rfloor>t2"

axiomatization where
  Xoap_t2: "\<lfloor>\<^bold>X oap\<rfloor>t2" and
  Xosp_t2: "\<lfloor>\<^bold>X osp\<rfloor>t2" and
  Xopr_t2: "\<lfloor>\<^bold>X opr\<rfloor>t2" and
  Xrv_t2:  "\<lfloor>\<^bold>X rv\<rfloor>t2" and
  Xosr_t2: "\<lfloor>\<^bold>X osr\<rfloor>t2" and
  Xpsr_t2: "\<lfloor>\<^bold>X psr\<rfloor>t2"

lemma only_Con_Leg_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_leg g)\<^bold>\<longrightarrow>(g \<^bold>= Congress)\<rfloor>t2"
  using unique_is_leg Con_Leg_t2 global_valid_def local_valid_def tallB_g_def
        tall_g_def tand_def teq_def timp_def
  by simp

lemma only_P_Exe_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_exe g)\<^bold>\<longrightarrow>(g \<^bold>= P)\<rfloor>t2"
  unfolding Defs using unique_is_exe P_Exe_t2
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def tand_def teq_def timp_def)

lemma only_Cou_Jud_t2: "\<lfloor>\<^bold>\<forall>\<^sub>g g. (is_jud g)\<^bold>\<longrightarrow>(g \<^bold>= Courts)\<rfloor>t2"
  unfolding Defs using unique_is_jud Cou_Jud_t2
  by (simp add: global_valid_def local_valid_def tallB_g_def tall_g_def tand_def teq_def timp_def)

theorem noDictatorship_t2: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t2"
  unfolding Defs using only_Con_Leg_t2 only_P_Exe_t2 only_Cou_Jud_t2 Dictatorship_def
  by (metis (mono_tags, lifting) g.distinct(3) local_valid_def tallB_g_def
      tall_g_def tand_def teq_def timp_def)

(* ---------------- 4.3.4 Time instance t3 ---------------- *)

lemma oap_t3: "\<lfloor>oap\<rfloor>t3" using Xoap_t2 local_valid_def tnext_def t2_s_t3 by auto
lemma osp_t3: "\<lfloor>osp\<rfloor>t3" using Xosp_t2 local_valid_def tnext_def t2_s_t3 by auto
lemma opr_t3: "\<lfloor>opr\<rfloor>t3" using Xopr_t2 local_valid_def tnext_def t2_s_t3 by auto
lemma rv_t3:  "\<lfloor>rv\<rfloor>t3"  using Xrv_t2  local_valid_def tnext_def t2_s_t3 by auto
lemma osr_t3: "\<lfloor>osr\<rfloor>t3" using Xosr_t2 local_valid_def tnext_def t2_s_t3 by auto
lemma psr_t3: "\<lfloor>psr\<rfloor>t3" using Xpsr_t2 local_valid_def tnext_def t2_s_t3 by auto

lemma amd2_val_t3: "\<lfloor>amd2\<rfloor>t3"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd2)\<rfloor>t2"
    using amd2_prop_t2 amd2_sup_rat_t2 local_valid_def tallB_s_def tall_s_def
          tand_def timp_def tnext_def psr_t2
    by auto
  thus "\<lfloor>amd2\<rfloor>t3"
    using local_valid_def tallB_s_def tall_s_def timp_def tnext_def rv_t3 t2_s_t3
    by auto
qed

theorem Dictatorship_t3: "\<lfloor>Dictatorship\<rfloor>t3"
proof -
  have "\<lfloor>is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P\<rfloor>t3"
    using amd2_val_t3 amd2_def
    by (simp add: local_valid_def tand_def)
  thus "\<lfloor>Dictatorship\<rfloor>t3"
    by (meson Dictatorship_def local_valid_def)
qed

(* ---------------- CONSISTENCY CHECK ----------------
   Everything above is vacuous if the axiom set is inconsistent, because an
   inconsistent theory proves every formula including Dictatorship_t3. The
   thesis checks this with Nitpick at each time instance; this is the t3 check,
   which subsumes the earlier ones since axioms are only ever added.

   Two independent tests:
     1. Nitpick must FIND a satisfying model that respects the user axioms.
     2. Nitpick must FAIL to find a counterexample-free proof of False, i.e.
        an attempt to prove False must not succeed.
   ------------------------------------------------------------------ *)

lemma T_basic_sat_t3: "True"
  nitpick[satisfy, user_axioms, show_all, format = 2, card time = 4, timeout = 300] oops

lemma consistency_False: "False"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

end
