__author__ = 'sbarma'


# IMPORT
from behave import *
from termcolor import cprint
from resources.lib import DataController
from resources.pages import *

# STEP MATCHER
use_step_matcher("re")


# STEPS
@given(u'User provides correct loan amount, rate and term')
def step_impl(context):
	if context.RUN == "Y":
		# get parameter values
		dr = DataController(context)
		amount = dr.getParamValue("Loan Amount")
		rate = dr.getParamValue("Rate")
		term = dr.getParamValue("Term")
		
		# calculate emi
		page = CalcEmiPage(context)
		page.navigate( context.config.userdata['WEBSITE'] )
		page.provide_loan_details( amount, rate, term )


@given(u'User provides incorrect loan amount, rate and term')
def step_impl(context):
	pass


@when(u'User wants to calculate payable emi')
def step_impl(context):
	if context.RUN == "Y":
		# click calculate emi
		page = CalcEmiPage(context)
		page.calculate_emi()


@then(u'System shows expected emi')
def step_impl(context):
	if context.RUN == "Y":
		# get parameter values
		dr = DataController(context)
		exp_emi = dr.getParamValue("Payable Emi")

		# assert payable emi
		page = CalcEmiPage(context)
		page.assert_payable_emi( exp_emi )


@then(u'System alerts user')
def step_impl(context):
	pass