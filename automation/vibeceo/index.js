import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { matchPaths } from './rules.js';

// Minimal runner that reads policy.yaml and logs loaded rules.
export default async function runner({ github, context, core }) {
  const policyFile = path.join(process.cwd(), 'automation', 'vibeceo', 'policy.yaml');
  let policy = {};
  try {
    policy = yaml.load(fs.readFileSync(policyFile, 'utf8')) || {};
  } catch (err) {
    core?.warning?.(`Failed to load policy: ${err.message}`);
  }
  const rules = policy.rules || [];
  core?.info?.(`VibeCEO loaded ${rules.length} rule(s) for event ${context.eventName}`);
  // Placeholder: actual decision logic to be implemented later.
  return { rules, matchPaths };
}
