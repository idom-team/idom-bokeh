import replace from "rollup-plugin-replace";

export default {
  input: ["dist/idom_bokeh.min.js", "dist/idom_bokeh.js"],
  output: {
      dir: "dist/",
      format: "es",
  },
  context: "this",
  plugins: [
    replace({
      "process.env.NODE_ENV": JSON.stringify("production"),
      preventAssignment: true,
    }),
    // Hacky workaround for avoiding __esExport
    replace({
      "__esExport(": "(",
      delimiters: ['', '']
    }),
  ],
};
