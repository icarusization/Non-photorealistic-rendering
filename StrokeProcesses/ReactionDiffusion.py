import Implement_For_RD as IR

class ReactionDiffusion:
    def __init__(self):
        self.neighbor=[]
        self.reaction=[]
        self.diffusion_rate=1.0
        self.diffusion_mode=0
        self.result=[] #the result after the iterations

    def set_iternum(self,iternum):
        self.iternum=iternum


    def set_neighbor(self,neighbor):
        # neighborlist:[[1,4,6,7],....]
        self.neighbor=neighbor

    def set_reaction(self,reaction):
        # reactionlist:[local property,...]
        self.reaction=reaction

    def set_diffusion(self,diffusion):
        self.diffusion_rate=diffusion

    def set_mode(self,mode):
        self.diffusion_mode=mode

    # Function usage: diffuse the property of some important stroke to the whole graph
    # Pay attention: You need to set the diffusion mode first. Now 0 is for size and orientation and 1 is for color
    # whose format is reaction = [(h, s, v),..]
    # Parameter Explain:
    #   i --- the number of property you want to diffuse e.g. reaction[..][i]
    #   size,orientation,color
    #   ratio --- the ratio of origin effect you want to remain (only bigger value will remain)
    #   dif --- diffusion rate
    def diffusion(self, ratio=1.0):
        eff = IR.get_value(self.reaction)

        if self.diffusion_mode==0:
            #eff = IR.pass_threshold(eff, ratio, self.diffusion_mode)
            eff = IR.iteration(self.iternum, eff, self.diffusion_rate, self.neighbor)

        if self.diffusion_mode==1:
            #eff = IR.pass_threshold(eff, ratio, self.diffusion_mode)
            eff = IR.iteration_color(self.iternum, eff, self.diffusion_rate, self.neighbor)

        self.result=eff
