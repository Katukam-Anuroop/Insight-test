import matplotlib.pyplot as plt
import tempfile
import os

def build_charts(df, chart_plan):
    chart_infos = []
    for chart in chart_plan:
        chart_type = chart['type'].lower()
        cols = chart['columns']
        title = chart.get('rationale', '') or f"{chart_type.title()}: {', '.join(cols)}"
        fig, ax = plt.subplots()
        img_path = tempfile.mktemp(suffix=".png")

        # Choose chart type
        if "bar" in chart_type:
            df[cols[0]].value_counts().plot(kind='bar', ax=ax)
            ax.set_xlabel(cols[0])
            ax.set_title(title)
        elif "hist" in chart_type:
            df[cols[0]].plot(kind='hist', bins=15, ax=ax, alpha=0.7)
            ax.set_xlabel(cols[0])
            ax.set_title(title)
        elif "scatter" in chart_type and len(cols) >= 2:
            df.plot.scatter(x=cols[0], y=cols[1], ax=ax)
            ax.set_xlabel(cols[0])
            ax.set_ylabel(cols[1])
            ax.set_title(title)
        elif "box" in chart_type:
            df[cols[0]].plot(kind='box', ax=ax)
            ax.set_title(title)
        else:
            plt.close(fig)
            continue  # skip unrecognized chart types

        plt.tight_layout()
        fig.savefig(img_path)
        plt.close(fig)
        chart_infos.append({
            "title": title,
            "type": chart_type,
            "columns": cols,
            "img_path": img_path,
            "rationale": chart.get('rationale', '')
        })
    return chart_infos
