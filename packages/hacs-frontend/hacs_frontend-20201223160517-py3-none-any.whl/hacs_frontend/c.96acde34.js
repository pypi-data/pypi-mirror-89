import{_ as t,H as s,h as o,l as e,c as i}from"./e.af80405f.js";import{m as n}from"./c.6decce02.js";import"./c.0bebe439.js";import{v as a}from"./c.065ede2d.js";import"./c.666ddf16.js";import"./c.7e459887.js";let r=t([i("hacs-about-dialog")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?o`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.narrow?"HACS":"Home Assistant Community Store"}
        hideActions
      >
        <div class="content">
          ${n.html(`\n**${e("dialog_about.integration_version")}:** | ${this.hacs.configuration.version}\n--|--\n**${e("dialog_about.frontend_version")}:** | ${a}\n**${e("common.repositories")}:** | ${this.repositories.length}\n**${e("dialog_about.installed_repositories")}:** | ${this.repositories.filter(t=>t.installed).length}\n\n**${e("dialog_about.useful_links")}:**\n\n- [General documentation](https://hacs.xyz/)\n- [Configuration](https://hacs.xyz/docs/configuration/start)\n- [FAQ](https://hacs.xyz/docs/faq/what)\n- [GitHub](https://github.com/hacs)\n- [Discord](https://discord.gg/apgchf8)\n- [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)\n- [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)\n\n***\n\n_Everything you find in HACS is **not** tested by Home Assistant, that includes HACS itself._\n_The HACS and Home Assistant teams do not support **anything** you find here._\n        `)}
        </div>
      </hacs-dialog>
    `:o``}}]}}),s);export{r as HacsAboutDialog};
