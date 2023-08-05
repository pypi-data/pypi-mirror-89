from odoo import models, api, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def create_account_payment_line(self):
        apoo = self.env['account.payment.order']
        result_payorder_ids = []
        action_payment_type = 'debit'
        for move_line in self:
            applicable_lines = move_line.filtered(
                lambda x: (
                    not x.reconciled and x.payment_mode_id.payment_order_ok and
                    x.account_id.internal_type in ('receivable', 'payable') and
                    not any(p_state in ('draft', 'open', 'generated')
                            for p_state in x.payment_line_ids.mapped('state'))
                )
            )
            payment_modes = applicable_lines.mapped('payment_mode_id')
            if not payment_modes:
                raise UserError(_(
                    "No Payment Mode on move line %s") % move_line.display_name)
            for payment_mode in payment_modes:
                payorder = apoo.search([
                    ('payment_mode_id', '=', payment_mode.id),
                    ('state', '=', 'draft')
                ], limit=1)
                new_payorder = False
                if not payorder:
                    payorder = apoo.create({
                        'payment_mode_id': payment_mode.id,
                    })
                    new_payorder = True  # noqa
                result_payorder_ids.append(payorder.id)
                action_payment_type = payorder.payment_type
                count = 0
                for line in applicable_lines.filtered(
                    lambda x: x.payment_mode_id == payment_mode
                ):
                    line.create_payment_line_from_move_line(payorder)
                    count += 1
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account_payment_order',
            'account_payment_order_%s_action' % action_payment_type)
        if len(result_payorder_ids) == 1:
            action.update({
                'view_mode': 'form,tree,pivot,graph',
                'res_id': payorder.id,
                'views': False,
                })
        else:
            action.update({
                'view_mode': 'tree,form,pivot,graph',
                'domain': "[('id', 'in', %s)]" % result_payorder_ids,
                'views': False,
                })
        return action
