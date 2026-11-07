from manim import *
# LaTeX なしで動く書き方 (Text と図形だけ)。MathTex/BarChart の軸数字は LaTeX が必要。
class Compare(Scene):
    def construct(self):
        t = Text("生成時間の比較 (秒)", font="Yu Gothic", font_size=44).to_edge(UP)
        self.play(Write(t))
        data = [("MOSS", 24.2, PINK), ("Anima", 28.3, BLUE)]
        for i, (name, v, c) in enumerate(data):
            y = 0.8 - i * 1.6
            bar = Rectangle(width=0.01, height=0.9, fill_color=c, fill_opacity=1, stroke_width=0).move_to([-4, y, 0], aligned_edge=LEFT)
            lab = Text(name, font_size=32).next_to(bar, LEFT)
            val = Text(f"{v}", font_size=32)
            self.add(lab, bar)
            self.play(bar.animate.stretch_to_fit_width(v / 4).move_to([-4, y, 0], aligned_edge=LEFT), run_time=1)
            val.next_to(bar, RIGHT); self.play(FadeIn(val))
        self.wait(0.5)
