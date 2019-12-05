odoo.define('sale_order_template_additional_clause.AcceptanceCheckbox', function (require) {
"use strict";

require('web.dom_ready');

$(document).ready(function () {
    var $accept_and_sign_sidebar = $(".js_accept_and_sign_sidebar");
    var $accept_and_pay_sidebar = $(".js_accept_and_pay_sidebar");
    var $accept_and_sign_primary = $(".js_accept_and_sign_primary");
    var $accept_and_pay_primary = $(".js_accept_and_pay_primary");

    var $div_note_requires_acceptance = $(".js_note_requires_acceptance");
    var $div_additional_clause_requires_acceptance = $(".js_additional_clause_requires_acceptance");

    var $note_requires_acceptance = $("#note_requires_acceptance");
    var $additional_clause_requires_acceptance = $("#additional_clause_requires_acceptance");

    if (!$accept_and_sign_sidebar.length && !$accept_and_pay_sidebar.length && !$accept_and_sign_primary.length && !$accept_and_pay_primary.length) {
        return $.Deferred().reject("DOM doesn't contain '.js_accept_and_*'");
    }

    var buttons_can_be_enabled = function(){
        if ($note_requires_acceptance.length) {
            if (!$note_requires_acceptance[0].checked) {
                return false;
            }
        }
        if ($additional_clause_requires_acceptance.length) {
            if (!$additional_clause_requires_acceptance[0].checked) {
                return false;
            }
        }
        return true;
    };

    var compute_buttons_clickability = function(){
        var to_enable = buttons_can_be_enabled();
        if (to_enable) {
            if ($accept_and_sign_sidebar.length) {
                $accept_and_sign_sidebar.removeClass("disabled");
            }
            if ($accept_and_pay_sidebar.length) {
                $accept_and_pay_sidebar.removeClass("disabled");
            }
            if ($accept_and_sign_primary.length) {
                $accept_and_sign_primary.removeClass("disabled");
            }
            if ($accept_and_pay_primary.length) {
                $accept_and_pay_primary.removeClass("disabled");
            }
            if ($div_note_requires_acceptance.length) {
                $div_note_requires_acceptance.hide();
            }
            if ($div_additional_clause_requires_acceptance.length) {
                $div_additional_clause_requires_acceptance.hide();
            }
        }
        else {
            if ($accept_and_sign_sidebar.length) {
                $accept_and_sign_sidebar.addClass("disabled");
            }
            if ($accept_and_pay_sidebar.length) {
                $accept_and_pay_sidebar.addClass("disabled");
            }
            if ($accept_and_sign_primary.length) {
                $accept_and_sign_primary.addClass("disabled");
            }
            if ($accept_and_pay_primary.length) {
                $accept_and_pay_primary.addClass("disabled");
            }
            if ($div_note_requires_acceptance.length) {
                $div_note_requires_acceptance.show();
            }
            if ($div_additional_clause_requires_acceptance.length) {
                $div_additional_clause_requires_acceptance.show();
            }
        }
    };

    $note_requires_acceptance.change(compute_buttons_clickability);
    $additional_clause_requires_acceptance.change(compute_buttons_clickability);
});
});
