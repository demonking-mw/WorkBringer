/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
import "./src/env.js";

/** @type {import("next").NextConfig} */
module.exports = {
    async rewrites() {
        return [
            {
                source: '/generate',
                destination: 'http://127.0.0.1:5000/generate'
            }
        ]
    }
};
