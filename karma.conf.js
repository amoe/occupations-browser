// Karma configuration
// Generated on Fri Jan 19 2018 12:35:45 GMT+0000 (GMT)

module.exports = function(config) {
  config.set({
    basePath: '',
      frameworks: ['mocha', 'karma-typescript'],
    files: [
        { pattern: 'test/*.ts' },
        // the SUT *must* be included here as below, or imports from the tests
        // will break
        { pattern: 'src/*.ts' }
        
    ],
    exclude: [
    ],
    preprocessors: {
        "**/*.ts": "karma-typescript"
    },
    reporters: ['progress'],
    port: 57233,
    colors: true,

    autoWatch: false,
    browsers: ['ChromeHeadless'],


    singleRun: false,
      concurrency: Infinity,

      // These are needed otherwise random .ts files will start showing up in
      // the build.
      karmaTypescriptConfig: {
          include: {
              mode: 'replace',
              values: ["src/*.ts", "test/*.ts"]
          },
          // This is required -- regular typescript uses a different module
          // system to karma-typescript
          compilerOptions: {
              module: "commonjs"
          },
          tsconfig: "./tsconfig.json"
      }
  })
}
