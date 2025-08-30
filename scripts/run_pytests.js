// Cross-platform pytest runner
import { spawnSync } from 'node:child_process';

const isWin = process.platform === 'win32';
const cmd = isWin ? 'pwsh' : 'bash';
const args = isWin ? ['-File', 'scripts/ps/test.ps1'] : ['scripts/test.sh'];

const result = spawnSync(cmd, args, { stdio: 'inherit' });
process.exit(result.status ?? 1);
