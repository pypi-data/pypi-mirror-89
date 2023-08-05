// This file is auto-generated from the corresponding file in /dev_mode
/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

import { PageConfig } from '@jupyterlab/coreutils';

import './style.js';

async function createModule(scope, module) {
  try {
    const factory = await window._JUPYTERLAB[scope].get(module);
    return factory();
  } catch(e) {
    console.warn(`Failed to create module: package: ${scope}; module: ${module}`);
    throw e;
  }
}

/**
 * The main entry point for the application.
 */
export async function main() {

   // Handle a browser test.
   // Set up error handling prior to loading extensions.
   var browserTest = PageConfig.getOption('browserTest');
   if (browserTest.toLowerCase() === 'true') {
     var el = document.createElement('div');
     el.id = 'browserTest';
     document.body.appendChild(el);
     el.textContent = '[]';
     el.style.display = 'none';
     var errors = [];
     var reported = false;
     var timeout = 25000;

     var report = function() {
       if (reported) {
         return;
       }
       reported = true;
       el.className = 'completed';
     }

     window.onerror = function(msg, url, line, col, error) {
       errors.push(String(error));
       el.textContent = JSON.stringify(errors)
     };
     console.error = function(message) {
       errors.push(String(message));
       el.textContent = JSON.stringify(errors)
     };
  }

  var JupyterLab = require('@jupyterlab/application').JupyterLab;
  var disabled = [];
  var deferred = [];
  var ignorePlugins = [];
  var register = [];


  const federatedExtensionPromises = [];
  const federatedMimeExtensionPromises = [];
  const federatedStylePromises = [];

  // Start initializing the federated extensions
  const extensions = JSON.parse(
    PageConfig.getOption('federated_extensions')
  );

  const queuedFederated = [];

  extensions.forEach(data => {
    if (data.extension) {
      queuedFederated.push(data.name);
      federatedExtensionPromises.push(createModule(data.name, data.extension));
    }
    if (data.mimeExtension) {
      queuedFederated.push(data.name);
      federatedMimeExtensionPromises.push(createModule(data.name, data.mimeExtension));
    }
    if (data.style) {
      federatedStylePromises.push(createModule(data.name, data.style));
    }
  });

  /**
   * Iterate over active plugins in an extension.
   *
   * #### Notes
   * This also populates the disabled, deferred, and ignored arrays.
   */
  function* activePlugins(extension) {
    // Handle commonjs or es2015 modules
    let exports;
    if (extension.hasOwnProperty('__esModule')) {
      exports = extension.default;
    } else {
      // CommonJS exports.
      exports = extension;
    }

    let plugins = Array.isArray(exports) ? exports : [exports];
    for (let plugin of plugins) {
      if (PageConfig.Extension.isDisabled(plugin.id)) {
        disabled.push(plugin.id);
        continue;
      }
      if (PageConfig.Extension.isDeferred(plugin.id)) {
        deferred.push(plugin.id);
        ignorePlugins.push(plugin.id);
      }
      yield plugin;
    }
  }

  // Handle the registered mime extensions.
  const mimeExtensions = [];
  if (queuedFederated.indexOf('@jupyterlab/javascript-extension') === -1) {
    try {
      let ext = require('@jupyterlab/javascript-extension');
      for (let plugin of activePlugins(ext)) {
        mimeExtensions.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/json-extension') === -1) {
    try {
      let ext = require('@jupyterlab/json-extension');
      for (let plugin of activePlugins(ext)) {
        mimeExtensions.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/pdf-extension') === -1) {
    try {
      let ext = require('@jupyterlab/pdf-extension');
      for (let plugin of activePlugins(ext)) {
        mimeExtensions.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/vega5-extension') === -1) {
    try {
      let ext = require('@jupyterlab/vega5-extension');
      for (let plugin of activePlugins(ext)) {
        mimeExtensions.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }

  // Add the federated mime extensions.
  const federatedMimeExtensions = await Promise.allSettled(federatedMimeExtensionPromises);
  federatedMimeExtensions.forEach(p => {
    if (p.status === "fulfilled") {
      for (let plugin of activePlugins(p.value)) {
        mimeExtensions.push(plugin);
      }
    } else {
      console.error(p.reason);
    }
  });

  // Handled the registered standard extensions.
  if (queuedFederated.indexOf('@jupyterlab/application-extension') === -1) {
    try {
      let ext = require('@jupyterlab/application-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/apputils-extension') === -1) {
    try {
      let ext = require('@jupyterlab/apputils-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/celltags-extension') === -1) {
    try {
      let ext = require('@jupyterlab/celltags-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/codemirror-extension') === -1) {
    try {
      let ext = require('@jupyterlab/codemirror-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/completer-extension') === -1) {
    try {
      let ext = require('@jupyterlab/completer-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/console-extension') === -1) {
    try {
      let ext = require('@jupyterlab/console-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/csvviewer-extension') === -1) {
    try {
      let ext = require('@jupyterlab/csvviewer-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/debugger-extension') === -1) {
    try {
      let ext = require('@jupyterlab/debugger-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/docmanager-extension') === -1) {
    try {
      let ext = require('@jupyterlab/docmanager-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/documentsearch-extension') === -1) {
    try {
      let ext = require('@jupyterlab/documentsearch-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/extensionmanager-extension') === -1) {
    try {
      let ext = require('@jupyterlab/extensionmanager-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/filebrowser-extension') === -1) {
    try {
      let ext = require('@jupyterlab/filebrowser-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/fileeditor-extension') === -1) {
    try {
      let ext = require('@jupyterlab/fileeditor-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/help-extension') === -1) {
    try {
      let ext = require('@jupyterlab/help-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/htmlviewer-extension') === -1) {
    try {
      let ext = require('@jupyterlab/htmlviewer-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/hub-extension') === -1) {
    try {
      let ext = require('@jupyterlab/hub-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/imageviewer-extension') === -1) {
    try {
      let ext = require('@jupyterlab/imageviewer-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/inspector-extension') === -1) {
    try {
      let ext = require('@jupyterlab/inspector-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/launcher-extension') === -1) {
    try {
      let ext = require('@jupyterlab/launcher-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/logconsole-extension') === -1) {
    try {
      let ext = require('@jupyterlab/logconsole-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/mainmenu-extension') === -1) {
    try {
      let ext = require('@jupyterlab/mainmenu-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/markdownviewer-extension') === -1) {
    try {
      let ext = require('@jupyterlab/markdownviewer-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/mathjax2-extension') === -1) {
    try {
      let ext = require('@jupyterlab/mathjax2-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/notebook-extension') === -1) {
    try {
      let ext = require('@jupyterlab/notebook-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/rendermime-extension') === -1) {
    try {
      let ext = require('@jupyterlab/rendermime-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/running-extension') === -1) {
    try {
      let ext = require('@jupyterlab/running-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/settingeditor-extension') === -1) {
    try {
      let ext = require('@jupyterlab/settingeditor-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/shortcuts-extension') === -1) {
    try {
      let ext = require('@jupyterlab/shortcuts-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/statusbar-extension') === -1) {
    try {
      let ext = require('@jupyterlab/statusbar-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/terminal-extension') === -1) {
    try {
      let ext = require('@jupyterlab/terminal-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/theme-dark-extension') === -1) {
    try {
      let ext = require('@jupyterlab/theme-dark-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/theme-light-extension') === -1) {
    try {
      let ext = require('@jupyterlab/theme-light-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/toc-extension') === -1) {
    try {
      let ext = require('@jupyterlab/toc-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/tooltip-extension') === -1) {
    try {
      let ext = require('@jupyterlab/tooltip-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/translation-extension') === -1) {
    try {
      let ext = require('@jupyterlab/translation-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/ui-components-extension') === -1) {
    try {
      let ext = require('@jupyterlab/ui-components-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }
  if (queuedFederated.indexOf('@jupyterlab/vdom-extension') === -1) {
    try {
      let ext = require('@jupyterlab/vdom-extension');
      for (let plugin of activePlugins(ext)) {
        register.push(plugin);
      }
    } catch (e) {
      console.error(e);
    }
  }

  // Add the federated extensions.
  const federatedExtensions = await Promise.allSettled(federatedExtensionPromises);
  federatedExtensions.forEach(p => {
    if (p.status === "fulfilled") {
      for (let plugin of activePlugins(p.value)) {
        register.push(plugin);
      }
    } else {
      console.error(p.reason);
    }
  });

  // Load all federated component styles and log errors for any that do not
  (await Promise.allSettled(federatedStylePromises)).filter(({status}) => status === "rejected").forEach(({reason}) => {
    console.error(reason);
  });

  const lab = new JupyterLab({
    mimeExtensions,
    disabled: {
      matches: disabled,
      patterns: PageConfig.Extension.disabled
        .map(function (val) { return val.raw; })
    },
    deferred: {
      matches: deferred,
      patterns: PageConfig.Extension.deferred
        .map(function (val) { return val.raw; })
    },
  });
  register.forEach(function(item) { lab.registerPluginModule(item); });
  lab.start({ ignorePlugins });

  // Expose global app instance when in dev mode or when toggled explicitly.
  var exposeAppInBrowser = (PageConfig.getOption('exposeAppInBrowser') || '').toLowerCase() === 'true';
  var devMode = (PageConfig.getOption('devMode') || '').toLowerCase() === 'true';

  if (exposeAppInBrowser || devMode) {
    window.jupyterlab = lab;
  }

  // Handle a browser test.
  if (browserTest.toLowerCase() === 'true') {
    lab.restored
      .then(function() { report(errors); })
      .catch(function(reason) { report([`RestoreError: ${reason.message}`]); });

    // Handle failures to restore after the timeout has elapsed.
    window.setTimeout(function() { report(errors); }, timeout);
  }

}

